"""W2-04 local math only: exact proposed matcher, not industrial evaluator.
Run from any directory; results are saved beside this script.
"""
from functools import lru_cache
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
import json, platform
import numpy as np
import scipy
from scipy.sparse import csr_array
from scipy.sparse.csgraph import maximum_bipartite_matching


def assign(gs, alerts, costs):
    """lex-offline-v1: min (-cardinality, sum cost, sorted pair tuple).
    Unique ASCII immutable IDs. Missing edges forbidden. Fraction costs exact.
    Exponential reference DP; deliberately not a production-scale claim.
    """
    assert len(gs) == len(set(gs)) and len(alerts) == len(set(alerts))
    gs, alerts = tuple(sorted(gs)), tuple(sorted(alerts))
    assert all(g in gs and a in alerts for g, a in costs)
    costs = {p: Fraction(v) for p, v in costs.items()}
    assert all(v >= 0 for v in costs.values())

    @lru_cache(None)
    def dp(i, mask):
        if i == len(gs):
            return (0, Fraction(0), ())
        options = [dp(i + 1, mask)]  # unmatched GT, no artificial edge
        for j, a in enumerate(alerts):
            if not (mask >> j & 1) and (gs[i], a) in costs:
                n, c, pairs = dp(i + 1, mask | (1 << j))
                options.append((n - 1, c + costs[gs[i], a], ((gs[i], a),) + pairs))
        return min(options)
    n, cost, pairs = dp(0, 0)
    return {"pairs": [list(p) for p in pairs], "TP": -n,
            "FP": len(alerts) + n, "FN": len(gs) + n, "cost": str(cost),
            "pair_costs": [str(costs[p]) for p in pairs]}


def greedy(gs, alerts, costs):
    used = set()
    pairs = []
    for a in alerts:  # explicitly caller-defined chronological order
        for g in gs:
            if g not in used and (g, a) in costs:
                used.add(g)
                pairs.append([g, a])
                break
    return pairs


def interval_edge(l, u, e_min, e_max, h, anchor, delivery, D,
                  known_active_at_delivery=True, possibly_active_at_delivery=True):
    """One episode, closed onset/end bound sets; state [s,e), deadline inclusive.
    h is first sufficient causal evidence; anchor must be known active evidence.
    Independent onset/end rectangular support only (additional constraints need Omega).
    """
    if not (h <= anchor <= delivery):
        return {"status": "forbidden_causal", "raw_delay_bounds": [delivery-u, delivery-l]}
    lo, hi = max(l, delivery-D), min(u, anchor, delivery)
    possible = lo <= hi and delivery < e_max and possibly_active_at_delivery
    definite = (u <= anchor <= delivery and delivery-l <= D and
                delivery < e_min and known_active_at_delivery)
    return {"status": "definite" if definite else "possible" if possible else "forbidden",
            "raw_delay_bounds": [delivery-u, delivery-l],
            "eligible_delay_bounds": [delivery-hi, delivery-lo] if possible else None}


def main():
    cases = {}
    def case(name, gs, als, edges, expected):
        got = assign(gs, als, edges)
        assert got["pairs"] == expected, (name, got)
        for pg in permutations(gs):
            for pa in permutations(als):
                assert assign(pg, pa, edges) == got
        cases[name] = got
    case("empty_both", [], [], {}, [])
    case("no_alerts", ["G1"], [], {}, [])
    case("no_gt", [], ["A1"], {}, [])
    edges = {("G1", "A1"): 0, ("G2", "A1"): 0, ("G1", "A2"): 1}
    case("greedy_cardinality_loss", ["G1", "G2"], ["A1", "A2"], edges,
         [["G1", "A2"], ["G2", "A1"]])
    cases["greedy_cardinality_loss"]["chronological_greedy"] = greedy(["G1", "G2"], ["A1", "A2"], edges)
    case("cardinality_before_cost", ["G1", "G2"], ["A1", "A2"],
         {("G1", "A1"): 0, ("G1", "A2"): 100, ("G2", "A1"): 100},
         [["G1", "A2"], ["G2", "A1"]])
    case("sum_delay_tie", ["G1", "G2"], ["A1", "A2"],
         {("G1", "A1"): 3, ("G1", "A2"): 4, ("G2", "A1"): 1, ("G2", "A2"): 2},
         [["G1", "A1"], ["G2", "A2"]])
    case("equal_iou_tie", ["G1", "G2"], ["P1", "P2"],
         {(g,a): Fraction(1,2) for g in ["G1", "G2"] for a in ["P1", "P2"]},
         [["G1", "P1"], ["G2", "P2"]])
    case("person_cardinality_before_iou", ["G1", "G2"], ["P1", "P2"],
         {("G1", "P1"): Fraction(1,10), ("G1", "P2"): Fraction(3,5), ("G2", "P1"): Fraction(3,5)},
         [["G1", "P2"], ["G2", "P1"]])
    case("duplicate_split_or_id_switch", ["G1"], ["A1", "A2"],
         {("G1", "A1"): 1, ("G1", "A2"): 2}, [["G1", "A1"]])
    case("wrong_person_or_class", ["G1"], ["A1"], {}, [])
    case("merged_two_entries", ["G1", "G2"], ["A1"], {("G1", "A1"): 1}, [["G1", "A1"]])
    case("safe_reset_second_alert", ["G1", "G2"], ["A1", "A2"],
         {("G1", "A1"): 1, ("G2", "A2"): 1}, [["G1", "A1"], ["G2", "A2"]])
    case("all_invalid", ["G1", "G2"], ["A1", "A2"], {}, [])
    # Exhaust all 512 labelled bipartite graphs, compare cardinality with installed
    # primary solver; costs affect only our second/third objectives.
    checked = 0
    gs, als = ["G1", "G2", "G3"], ["A1", "A2", "A3"]
    for bits in product([0,1], repeat=9):
        costs = {(gs[i], als[j]): (i+2*j)%4 for i in range(3) for j in range(3) if bits[3*i+j]}
        k = assign(gs, als, costs)["TP"]
        graph = csr_array(np.array(bits).reshape(3,3))
        assert k == int(np.sum(maximum_bipartite_matching(graph, perm_type="column") >= 0))
        checked += 1
    # Prove second/third objectives with an independently enumerated permutation
    # oracle over partial injections for all same 512 graphs.
    def brute(gs, als, costs):
        options=[]
        for choices in product([None] + als, repeat=len(gs)):
            selected=[a for a in choices if a is not None]
            if len(set(selected)) != len(selected): continue
            pairs=tuple((g,a) for g,a in zip(gs,choices) if a is not None)
            if all(p in costs for p in pairs):
                options.append((-len(pairs), sum((Fraction(costs[p]) for p in pairs), Fraction(0)), pairs))
        return min(options)
    for bits in product([0,1], repeat=9):
        costs = {(gs[i], als[j]): (i+2*j)%4 for i in range(3) for j in range(3) if bits[3*i+j]}
        result = assign(gs,als,costs)
        oracle = brute(gs,als,costs)
        assert (-result["TP"], Fraction(result["cost"]), tuple(map(tuple,result["pairs"]))) == oracle
    intervals = {
        "exact_deadline_equal": interval_edge(0,0,20,20,0,0,5,5),
        "onset_straddles_deadline": interval_edge(0,2,20,20,2,2,6,5),
        "before_sufficient_evidence": interval_edge(0,2,20,20,2,1,1,5),
        "known_short_end": interval_edge(0,0,2,2,0,0,2,5),
        "short_success": interval_edge(0,0,2,2,0,0,1,5),
        "uncertain_end": interval_edge(0,0,3,5,0,0,4,5),
        "unknown_gap_delivery": interval_edge(0,0,10,10,0,1,4,5,False,True),
        "late_result": interval_edge(0,0,20,20,0,0,6,5),
    }
    expected={"exact_deadline_equal":"definite", "onset_straddles_deadline":"possible",
              "before_sufficient_evidence":"forbidden_causal", "known_short_end":"forbidden",
              "short_success":"definite", "uncertain_end":"possible",
              "unknown_gap_delivery":"possible", "late_result":"forbidden"}
    assert {k:v["status"] for k,v in intervals.items()} == expected
    # Shared annotation constraint: s1=theta, s2=theta+1; theta in [0,10].
    # Each person keyed only to its own alert d1=1,d2=11; D=1.
    joint=[]
    for theta in range(11):
        n = int(0 <= 1-theta <= 1) + int(0 <= 11-(theta+1) <= 1)
        joint.append({"theta":theta,"TP":n})
    assert max(x["TP"] for x in joint)==1
    # Two equally truncated episodes: one observed success, one unobserved outcome.
    # Exclude both from complete-follow-up recall; retain both for end-of-recording.
    censoring = {
        "right_censored_success": {"onset":28,"D":5,"F":30,"delivery":29,"complete_followup":False,"primary_GT":0,"primary_alerts":0,"quarantine_GT":1,"observed_success":1},
        "right_censored_no_success": {"onset":28,"D":5,"F":30,"delivery":None,"complete_followup":False,"primary_GT":0,"primary_alerts":0,"quarantine_GT":1,"observed_success":0},
        "short_complete_no_alert": {"onset":0,"end":2,"D":5,"F":2,"complete_followup":True,"primary_GT":1,"primary_alerts":0,"FN":1},
        "right_end_censored_deadline_complete": {"onset":0,"D":5,"F":6,"end":None,"complete_followup":True,"primary_GT":1,"primary_alerts":0,"FN":1},
    }
    assert sum(x["primary_GT"] for x in list(censoring.values())[:2]) == 0
    assert sum(x["observed_success"] for x in list(censoring.values())[:2]) == 1
    person_states = {"person_pairs":[["GA","PA"],["GB","PB"]],"GT":{"GA":"N","GB":"V"},
                     "prediction":{"PA":"V","PB":"N"},"N_known":2,"TP_V":0,"FP_V":1,"FN_V":1}
    assert assign(["GA","GB"],["PA","PB"],{("GA","PA"):0,("GB","PB"):0})["pairs"] == person_states["person_pairs"]
    out={"protocol":"lex-offline-v1", "python":platform.python_version(),"scipy":scipy.__version__,
         "scope":"Executed local mathematical fixtures; no model/application/device benchmark",
         "assignment_cases":cases,"exhaustive_3x3_graphs":checked,
         "independent_partial_injection_oracle_graphs":512,
         "input_permutation_invariance":"all permutations of each named graph passed",
         "interval_edges":intervals,"joint_constraint_example":joint,
         "censoring":censoring,"wrong_person_state_after_independent_matching":person_states}
    Path(__file__).with_name("results.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps({"named_assignment_cases":len(cases),"exhaustive_graphs":checked,
                      "interval_cases":len(intervals),"status":"all assertions passed"}))

if __name__ == "__main__": main()
