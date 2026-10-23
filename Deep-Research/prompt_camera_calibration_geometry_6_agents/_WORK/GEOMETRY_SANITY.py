"""Small analytic illustration, not a camera/video benchmark. Standard library only."""
import json

h, f = 4.0, 1000.0
rows = []
for depth in (8.0, 20.0, 40.0):
    v = f * h / depth
    reconstructed = f * h / (v + 1.0)
    rows.append({"true_depth_m": depth, "floor_v_px_from_horizon": v,
                 "mapped_depth_after_plus_1px_m": reconstructed,
                 "absolute_depth_error_m": abs(reconstructed-depth)})

depth, elevated_height = 8.0, 1.0
v_elevated = f * (h-elevated_height) / depth
result = {
    "status": "synthetic_analytic_illustration_only",
    "camera": {"height_m": h, "focal_length_px": f, "axis": "horizontal", "distortion": "none"},
    "formula": "v=f*(h-z)/Z; applying floor inverse gives Z_hat=h*Z/(h-z)",
    "one_pixel_error": rows,
    "elevated_point": {"true_depth_m": depth, "height_above_floor_m": elevated_height,
                       "pixel_v": v_elevated, "wrong_floor_depth_m": f*h/v_elevated},
    "sampling": {"path": "x(t)=2t m, t in [0,1] s", "open_zone_m": [0.8, 1.2],
                 "occupancy_interval_s": [0.4, 0.6], "occupancy_duration_s": 0.2,
                 "sample_times_s": [0.0, 1.0], "sample_positions_m": [0.0, 2.0],
                 "direct_in_zone_sample_count": 0,
                 "caveat": "Segment interpolation infers crossing only under an added trajectory assumption."}
}
assert abs(result["elevated_point"]["wrong_floor_depth_m"] - 32/3) < 1e-12
assert rows[0]["absolute_depth_error_m"] < rows[1]["absolute_depth_error_m"] < rows[2]["absolute_depth_error_m"]
print(json.dumps(result, ensure_ascii=False, indent=2))
