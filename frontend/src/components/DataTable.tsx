import type { ReactNode } from "react";

interface Column<T> {
  title: string;
  cell: (row: T) => ReactNode;
}

type Row = { id: number };
type Props<T> = { columns: Column<T>[]; rows: T[]; empty: string };

// The generic overload types the screens; the plain implementation keeps the trace line of 6.7.
export function DataTable<T extends Row>(props: Props<T>): ReactNode;
export function DataTable({ columns, rows, empty }: Props<Row>): ReactNode {
  if (rows.length === 0) return <p className="empty">{empty}</p>;
  return (
    <table className="data-table">
      <thead>
        <tr>
          {columns.map((c) => (
            <th key={c.title}>{c.title}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.id}>
            {columns.map((c) => (
              <td key={c.title}>{c.cell(row)}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
