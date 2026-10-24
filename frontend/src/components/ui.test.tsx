import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Button, ConfirmDialog, Icon, Kpi, Segmented, Sparkline, ToastProvider, useToast } from "./ui";

afterEach(cleanup);

function ToastButton() {
  const toast = useToast();
  return <button onClick={() => toast({ title: "Сохранено", tone: "green" })}>Показать</button>;
}

describe("design system primitives", () => {
  it("renders lucide icons behind the old Icon API", () => {
    const { container } = render(<Icon name="camera" />);
    expect(container.querySelector("svg")?.getAttribute("aria-hidden")).toBe("true");
  });
  it("segmented control reports the picked option and marks it pressed", () => {
    const onChange = vi.fn();
    render(<Segmented label="Уровень" value="all" onChange={onChange} options={[{ id: "all", label: "Все" }, { id: "red", label: "Тревога", count: 3 }]} />);
    expect(screen.getByRole("button", { name: "Все" }).getAttribute("aria-pressed")).toBe("true");
    fireEvent.click(screen.getByRole("button", { name: /Тревога/ }));
    expect(onChange).toHaveBeenCalledWith("red");
  });
  it("confirm dialog confirms, cancels on Escape and renders nothing when closed", () => {
    const onConfirm = vi.fn(); const onCancel = vi.fn();
    const { rerender } = render(<ConfirmDialog open title="Закрыть событие?" onConfirm={onConfirm} onCancel={onCancel} />);
    fireEvent.click(screen.getByRole("button", { name: "Подтвердить" }));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(onConfirm).toHaveBeenCalledOnce();
    expect(onCancel).toHaveBeenCalledOnce();
    rerender(<ConfirmDialog open={false} title="Закрыть событие?" onConfirm={onConfirm} onCancel={onCancel} />);
    expect(screen.queryByRole("dialog")).toBeNull();
  });
  it("toasts appear under the provider and disappear on close", () => {
    render(<ToastProvider><ToastButton /></ToastProvider>);
    fireEvent.click(screen.getByRole("button", { name: "Показать" }));
    expect(screen.getByText("Сохранено")).toBeTruthy();
    act(() => { fireEvent.click(screen.getByRole("button", { name: "Закрыть" })); });
    expect(screen.queryByText("Сохранено")).toBeNull();
  });
  it("button shows busy state; KPI and sparkline render values only", () => {
    render(<><Button busy>Сохранить</Button><Kpi label="Событий" value={57} spark={<Sparkline values={[1, 3, 2]} label="По дням" />} /></>);
    expect(screen.getByRole("button", { name: "Сохранить" }).getAttribute("aria-busy")).toBe("true");
    expect(screen.getByText("57")).toBeTruthy();
    expect(screen.getByRole("img", { name: "По дням" })).toBeTruthy();
  });
});
