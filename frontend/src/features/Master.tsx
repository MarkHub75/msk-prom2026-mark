import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useApi } from "../api/useApi";
import { useRole } from "../roles";
import { useUpdates } from "../components/AppShell";
import { EventFeed } from "../components/EventFeed";
import { Empty, ErrorNotice, Icon, Loading, PageHeading, PanelHeading, time } from "../components/ui";

export function MasterPage() {
  const updates = useUpdates(); const [role] = useRole();
  const inbox=useApi(()=>api.GET("/api/master/inbox"),[updates,role]);
  return <div className="master-inbox" data-testid="master-inbox"><PageHeading title="Мои поручения" meta={inbox.data?`Состояние на ${time(inbox.data.server_now)}`:"Рабочее место мастера"}><button className="button button-small" onClick={inbox.reload} disabled={inbox.loading}>Обновить</button></PageHeading>{inbox.error?<ErrorNotice error={inbox.error} retry={inbox.reload} />:!inbox.data?<Loading />:<><div className="master-inbox-layout"><section><PanelHeading aside={`${inbox.data.active.length}`}>В работе и ожидают принятия</PanelHeading>{inbox.data.active.length?<EventFeed events={inbox.data.active} master />:<Empty title="Активных поручений нет" text="Новые переданные события появятся здесь." />}</section><section className="master-resolved"><PanelHeading aside={`${inbox.data.recent_resolved.length}`}>Недавно завершено</PanelHeading>{inbox.data.recent_resolved.length?<EventFeed events={inbox.data.recent_resolved} master compact />:<div className="quiet-empty">Завершённых поручений пока нет.</div>}<Link className="text-link" to="/master/shift">Хронология смены <Icon name="arrow" size={16} /></Link></section></div><div className="master-instruction"><span>01</span><p>Примите поручение.</p><span>02</span><p>Проверьте участок.</p><span>03</span><p>Сообщите о принятых мерах.</p></div></>}</div>;
}
export function ShiftPage() {
  const updates=useUpdates(); const [role]=useRole();
  const inbox=useApi(()=>api.GET("/api/master/inbox"),[updates,role]);
  const events=inbox.data?[...inbox.data.active,...inbox.data.recent_resolved].sort((a,b)=>b.published_at.localeCompare(a.published_at)):[];
  return <div className="master-shift"><PageHeading title="Моя смена" meta="Хронология поручений мастера" />{inbox.error?<ErrorNotice error={inbox.error} retry={inbox.reload} />:!inbox.data?<Loading />:<><PanelHeading aside={`${events.length} событий`}>Поручения за доступный период</PanelHeading><EventFeed events={events} master /></>}<p className="muted shift-note">Показаны активные и недавно завершённые поручения из серверного входящего списка. Итоговая статистика смены в этом этапе не реализована.</p></div>;
}
