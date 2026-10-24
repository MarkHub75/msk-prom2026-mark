export function StubNotice({ slice, title }: { slice: number; title: string }) {
  return (
    <section className="stub">
      <h1>{title}</h1>
      <p>Экран появится в слайсе {slice}</p>
    </section>
  );
}
