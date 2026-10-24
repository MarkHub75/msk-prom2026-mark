import { describe, expect, it } from "vitest";
import {
  applyH, centroid, convexHull, fitHomography, fitRmse, gridPreview, hitEdge, hitVertex, insertVertex, moveVertex, overrides,
  parseNumber, pointInPolygon, polygonArea, removeVertex, toNorm, translate, zoneProblem, type Pt,
} from "./geometry";
import { calibrationBody } from "./CalibrationTab";
import { paramProblems } from "./CameraRulesTab";

const square: Pt[] = [[0.1, 0.1], [0.5, 0.1], [0.5, 0.5], [0.1, 0.5]];

describe("geometry helpers", () => {
  it("maps client points to the normalized frame and clamps them", () => {
    const rect = { left: 100, top: 50, width: 800, height: 400 };
    expect(toNorm(500, 250, rect)).toEqual([0.5, 0.5]);
    expect(toNorm(0, 1000, rect)).toEqual([0, 1]);
  });

  it("measures polygons", () => {
    expect(polygonArea(square)).toBeCloseTo(0.16);
    expect(centroid(square)[0]).toBeCloseTo(0.3);
    expect(pointInPolygon([0.3, 0.3], square)).toBe(true);
    expect(pointInPolygon([0.7, 0.3], square)).toBe(false);
  });

  it("hits vertices and edges in pixels", () => {
    expect(hitVertex(square, [0.502, 0.1], 1000, 1000)).toBe(1);
    expect(hitVertex(square, [0.3, 0.3], 1000, 1000)).toBe(-1);
    expect(hitEdge(square, [0.3, 0.103], 1000, 1000, true)).toBe(0);
    expect(hitEdge(square, [0.1, 0.3], 1000, 1000, true)).toBe(3);
    expect(hitEdge(square, [0.1, 0.3], 1000, 1000, false)).toBe(-1);
  });

  it("edits vertices", () => {
    expect(insertVertex(square, 0, [0.3, 0.1])[1]).toEqual([0.3, 0.1]);
    expect(removeVertex(square, 0)).toHaveLength(3);
    expect(moveVertex(square, 2, [1.4, -0.2])[2]).toEqual([1, 0]);
    // A shape moved past the edge stops at the frame.
    expect(translate(square, 0.9, 0)).toEqual([[0.6, 0.1], [1, 0.1], [1, 0.5], [0.6, 0.5]]);
  });

  it("prechecks zones with the backend rules", () => {
    expect(zoneProblem("polygon", square)).toBeNull();
    expect(zoneProblem("polygon", square.slice(0, 2))).toBe("Полигон: от 3 до 32 точек");
    expect(zoneProblem("polygon", [[0, 0], [0.5, 0.5], [1, 1]])).toBe("Полигон без площади: точки на одной прямой");
    expect(zoneProblem("line", [[0.1, 0.1], [0.1, 0.1]])).toBe("Линия — ровно 2 точки");
    expect(zoneProblem("line", [[0.1, 0.1], [0.4, 0.2]])).toBeNull();
  });

  it("parses Russian numbers", () => {
    expect(parseNumber("2,5")).toBe(2.5);
    expect(parseNumber(" -1.25 ")).toBe(-1.25);
    expect(parseNumber("")).toBeNull();
    expect(parseNumber("2,5 м")).toBeNull();
  });

  it("fits a homography that maps the floor points to meters", () => {
    const image: Pt[] = [[0.25, 0.55], [0.75, 0.55], [0.9, 0.95], [0.1, 0.95]];
    const world: Pt[] = [[0, 0], [6, 0], [6, 4], [0, 4]];
    const h = fitHomography(image, world)!;
    expect(h).not.toBeNull();
    const q = applyH(h, image[2])!;
    expect(q[0]).toBeCloseTo(6, 6);
    expect(q[1]).toBeCloseTo(4, 6);
    expect(fitRmse(h, image, world)).toBeCloseTo(0, 6);
    // 7 vertical + 5 horizontal 1 m lines, each sampled in 16 pieces.
    expect(gridPreview(h, world)).toHaveLength(12 * 16);
    expect(convexHull([...image, [0.5, 0.7]])).toHaveLength(4);
  });

  it("builds the calibration body or names the problem", () => {
    const row = (x: number, y: number, mx: string, my: string) => ({ image: [x, y] as Pt, x: mx, y: my });
    expect(calibrationBody({ fit: [row(0, 0, "0", "0")], control: [] }).problem).toBe("Нужно от 4 до 8 точек");
    const fit = [row(0.1, 0.1, "0", "0"), row(0.9, 0.1, "6", "0"), row(0.9, 0.9, "6", "4"), row(0.1, 0.9, "0", "")];
    expect(calibrationBody({ fit, control: [] }).problem).toMatch(/Заполните метры/);
    fit[3].y = "4,5";
    expect(calibrationBody({ fit, control: [row(0.5, 0.5, "3", "2")] }).body).toEqual({
      image_points: [[0.1, 0.1], [0.9, 0.1], [0.9, 0.9], [0.1, 0.9]],
      world_points: [[0, 0], [6, 0], [6, 4], [0, 4.5]],
      control_points: [{ image: [0.5, 0.5], world: [3, 2] }],
    });
  });

  it("sends only overrides and checks ranges of rule params", () => {
    expect(overrides({ hold_s: 1, red_hold_s: 0.5 }, { hold_s: 2, red_hold_s: 0.5 })).toEqual({ hold_s: 2 });
    const s = { params: [{ key: "hold_s", title: "Удержание", unit: "с", min: 0, max: 60, default: 1 }] } as Parameters<typeof paramProblems>[0];
    expect(paramProblems(s, { hold_s: "61" })).toEqual({ hold_s: "От 0 до 60" });
    expect(paramProblems(s, { hold_s: "abc" })).toEqual({ hold_s: "Нужно число" });
    expect(paramProblems(s, { hold_s: "1,5" })).toEqual({});
  });
});
