import { Link } from "react-router-dom";
import { useRole } from "../roles";
import { menuFor } from "../nav";
import { PageHeading } from "./ui";
export function StubNotice({ slice, title }: { slice: number; title: string }) {
  const [role] = useRole();
  return <><PageHeading title={title} meta="Область текущей роли" /><section className="scope-notice"><span className="scope-number">{String(slice).padStart(2, "0")}</span><div><h2>Раздел запланирован</h2><p>Этот экран относится к следующему этапу реализации. В текущей версии доступны сигнальный пост оператора, разбор события, просмотр записи и поручения мастера.</p><Link className="button" to={menuFor(role)[0]?.path ?? "/operator"}>К разделам роли</Link></div></section></>;
}
