# W2A access log and evidence limits

Checked 2026-10-23 around 10:00–10:08 Europe/Moscow. All actions read-only; no authentication or external messages.

## PDF
- Fresh TinyFish fetch_content, format=json, ttl=0, validators requested: full extracted content delivered; no PDF bytes, ETag or Last-Modified for PDF delivered. author field returned Elena Belozerova, published_date=null. Author field is extraction metadata, not proof of legal authorship/signature.
- urllib explicit TLS1.2 context (distinct from W1 default requests/schannel), 25s timeout, request to exact official URL failed SSL UNEXPECTED_EOF_WHILE_READING before PDF bytes. Exact attempt/result saved PDF_RETRIEVAL.json. No original hash exists.
- web screenshot calls pageno6/8/10 returned only text reference stubs. Saved PDF_SCREENSHOT_TOOL_RESPONSE.json. No image was delivered/viewed.
- Browser FAQ run attempted official PDF: terminal reports PDF inspection timeout.
- PDF_FRESH_TEXT was compared to W1 PDF_FULL_TEXT after whitespace removal only; equal=true in TEXT_COMPARISON.json. This checks extracts only.

## FAQ/site
- SITE_FETCH.json contains cleaned body HTML, links and HTTP metadata, not original page scripts/FAQ DOM. Request ttl=0.
- Last-Modified Thu, 22 Oct 2026 14:52:31 GMT, ETag "2d17a2-65e6f03645547-gzip". These apply to site HTTP response, not PDF or semantic rule revision.
- New TinyFish browser run f42b5460-74a1-472d-adfd-b7c6e7af6268, start07:01:39Z, finish07:05:13Z,20steps,214s, completed. capture_config html/screenshots/snapshots requested.
- Terminal says screenshot captures performed. Actual returned content is text only and no capture files/URLs; cannot claim direct independent image/HTML preservation. New agent transcript preserved in FAQ_BROWSER_TERMINAL.json and FAQ_BROWSER_EXTRACT.txt.
- Terminal English summary incorrectly says7technology criteria while Russian list has6. It also paraphrases/summarises some answers. Do not use English summary or agent headings as exact official text.
- get_run was used once after completion to retrieve persistent terminal result/metadata, not progress polling; no capture URLs appeared. Tool discovery found no screenshot/artifact retrieval tool.

## Public access paths
- https://lk2026.otkroimosprom.ru/lk/event/115 web open: title Открой#Моспром, Total lines0. Login not attempted. Rendering/extraction limit, not confirmed absence of content nor confirmed authentication requirement.
- https://vk.ru/hack_mosprom web open: non-retryable error. Posts not read.
- https://max.ru/channel_hack_mosprom public landing read, linked by official current site. Its browser link https://web.max.ru/channel_hack_mosprom yields0lines; posts/attachments not read. No login.
- Site footer exposes PDF/privacy, current site links include mts-link.ru. No published jury memo/assessment form or specific meeting role was delivered.
- Browser run checked relevant FAQ/footer; no specific VC platform name found in defence answer.

## Targeted searches
Saved SEARCH_TOOLING.json and SEARCH_FORMS.json:
- site:hackathon2026.otkroimosprom.ru "памятка"
- "Моспром" "2026" "платные"
- "Моспром" "2026" "МТС" "защита"
- "hackathon2026.otkroimosprom.ru" "памятка жюри"
- "Моспром" "2026" "оценочная форма"
- "Моспром" "2026" "нулевой результат"
- "Моспром" "2026" "видеосвязь"

Results did not supply a current primary clarification. Irrelevant results were not treated as supporting sources. This is a bounded search result, not evidence that no internal memo/exception exists.

## Remaining closure artifacts
Original PDF bytes/hash/visual critical pages; delivered FAQ DOM/screenshots; current jury memo/form; category-specific resource/recording permissions and video rights; actual CP receipt/zero result rules; actual defence URL/product/mode/role and viewer test. Owners and questions are in W2/W2A_BINDING_RULES.md.

