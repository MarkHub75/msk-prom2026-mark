import { Icon } from "./ui";
import "../styles/pwa.css";

/** No answer from the server: instead of stale alarms (or a white screen) the app says so and keeps checking. */
export function OfflineScreen({ network, onRetry }: { network: boolean; onRetry: () => void }) {
  return <div className="pwa-offline" role="alert" data-testid="offline-screen">
    <span className="pwa-offline-icon"><Icon name="wifi-off" size={34} /></span>
    <h1>Нет связи с сервером — данные не показываются</h1>
    <p>{network ? "Сервер не отвечает." : "Телефон без сети."} Устаревшие тревоги опаснее пустого экрана: как только связь вернётся, данные появятся сами.</p>
    <button className="pwa-offline-retry" onClick={onRetry}>Проверить связь</button>
  </div>;
}
