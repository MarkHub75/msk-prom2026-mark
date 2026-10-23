# W2-07 primary source access notes

Access date: 2026-10-23, 20:04–20:06 UTC. These are short paraphrases, not full copies.

## NIST / SEMATECH e-Handbook §8.4.5.1

URL: https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm

Web tool opened actual HTML successfully. Python byte retrieval returned HTTP 403; this is a tool/path distinction, not evidence of a closed source. No local HTML snapshot exists. Locator: “Confidence Interval Equation and Zero Fails Case”, web lines 100–105; “How To Use”, lines 23–32.

Under the constant-rate HPP/exponential model, zero observed failures over fixed total time T gives one-sided lower MTBF T/(-ln alpha). The lower bound corresponds to confidence 1-alpha. The table columns headed as two-sided confidence use alpha/2 tails; do not read their zero-failure row as the same nominal one-sided confidence. Publication/update date not established. Author organization: NIST/SEMATECH. Not a CV deployment study.

## NIST / SEMATECH e-Handbook §1.3.6.6.19

URL: https://www.itl.nist.gov/div898/handbook/eda/section3/eda366j.htm

Web opened actual HTML; Python retrieval HTTP 403. Locator: Probability Mass Function, web line 8. Poisson event counts over an interval have mass exp(-mu) mu^x / x!, hence probability of zero exp(-mu). Here mu is interval expected count; rate times exposure is our application. Publication/update date unknown.

## Cameron and Miller 2015

URL: https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf

Author PDF opened and text read by web: JHR 50(2), 317–372 (2015); §VI.A PDF pages 25–26, §VI.C.3 PDF page 29. Few clusters can produce narrow intervals and overrejection, and number of observations per cluster does not substitute for the number of independent clusters. This is regression methodology, not an exact event/AP interval recipe. Byte download via Python failed WinError 10054. Web screenshot calls returned reference strings without usable image blocks in functions runtime, so screenshots were requested but not personally visually inspected; no tables/numerical simulation results are used here. W1-12-S08 is the earlier read of this source.

## Local case

Original: _WORK/INPUT/CASE_LINQ.pdf; SHA256 recorded by root: 7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e.

Personally viewed existing large PNG renders of case pages 5, 7, 13, 19 from ../LinQ-case-analytics-research/_WORK/CASE_PAGE_{5,7,13,19}.png. These were not newly rendered in W2-07. Requirements: prompt useful incident alerts, duplicate suppression, measured LinQ inference. No numeric task-quality acceptance budget was found on those pages. Existing root notes cover the whole case. Source publication date/public URL unknown.
