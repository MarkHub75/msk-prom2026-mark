# W1A: доступ, статус оригиналов и provenance

Дата получения: 2026-10-23, начало09:31 Europe/Moscow. Отдельная дата публикации/редакции сайта, FAQ и PDF не установлена; год PDF2026. Все действия только чтение; сообщения организаторам, вход в аккаунт, размещение контента не выполнялись.

## Успех

- web open официального сайта и24-страничного PDF: сохранены raw текстовые ответы WEB_CAPTURE*.txt; PDF_PAGE_EXCERPTS.txt объединяет строки с локаторами страниц. Полный текст PDF через TinyFish fetch сохранён PDF_FULL_TEXT.txt, raw ответ PDF_TINYFISH.json.
- TinyFish fetch сайта не включал динамические ответы FAQ даже при format=html (файл TINYFISH_HTML.json содержит фактически очищенный текст).
- TinyFish run_web_automation прочитал FAQ через браузер и вернул terminal completed после201с, runId f09dcf0f-04e6-4a24-95ab-43d30cb60861. Raw FAQ_BROWSER_FINAL.json, читаемая распаковка FAQ_FULL_TEXT.txt. FAQ_BROWSER.json — промежуточное running; FAQ_READABLE.txt — техническая JSON-распаковка, для чтения лучше FAQ_FULL_TEXT.txt. Английский concluding summary browser-agent не использовался вместо русских ответов.
- LICENSE_CAPTURE.txt: официальный raw файл LICENSE Ultralytics содержит GNU AGPL v3 от19.11.2007. Использование изменяемого main фиксируется явно; commit не получен, лицензионный пример не равен проверке стека команды.

## Неудачные пути, не скрывать

- PowerShell Invoke-WebRequest HTTPS сайта/PDF: «Базовое соединение закрыто: Непредвиденная ошибка при передаче».
- Python requests.get HTTPS сайта: SSLError UNEXPECTED_EOF_WHILE_READING; MaxRetryError. Ошибка произошла до получения байтов сайта, PDF в этом цикле не достигнут.
- curl.exe -I HTTPS PDF: (35) schannel: failed to receive handshake, SSL/TLS connection failed.
- curl.exe -L HTTP PDF: (52) Empty reply from server. В папке нет файла с именем polozhenie-mosprom-2026.pdf; он не получен.
- cua.createBrowserTab chrome: Browser is not available: chrome. cua.getState: apps=[], browsers=[]. Встроенный browser-channel отсутствовал, но это не отсутствие браузерного инструмента вообще: TinyFish отдельный канал сработал.
- web screenshot PDF с.8,9,10,11,14: обёртка вернула текстовые ссылки без доступных изображений; визуальная проверка не выполнена.
- https://lk2026.otkroimosprom.ru/lk/event/115 через web: Total lines:0. Содержимое ЛК не прочитано; неизвестно, требует ли он логина для каждого нужного документа.
- www.gnu.org/licenses/agpl-3.0.html, .en.html, .txt через web:400 Timeout fetching; raw LICENSE официального репозитория сработал.

## Ограничение и следующий путь

Байты оригинального PDF, его хеш и визуально проверенные страницы остаются задачей W2 из другой работающей среды. Доступное полное извлечение не обозначать оригиналом. Отсутствие ответа по формуле, платному AI или разрешению записи — точные неизвестные публичных прочитанных документов, не доказательство отсутствия внутренних правил.
