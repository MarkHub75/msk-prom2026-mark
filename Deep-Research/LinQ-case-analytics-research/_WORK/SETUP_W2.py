from pathlib import Path
import re
root=Path(__file__).resolve().parent.parent
w=root/'_WORK'
brief=(w/'RESEARCH_BRIEF.md').read_text(encoding='utf-8')
handoff=(w/'CRITIC_HANDOFF.md').read_text(encoding='utf-8')
critic=(root/'CRITIC.md').read_text(encoding='utf-8')
sections=re.split(r'(?m)^## W2-',handoff)
names=['OPERATIONAL_CONTEXT','DIRECT_HSE_WORKFLOW','BEHAVIORAL_COMPARISON','SECTOR_STATISTICS_METRICS','DEMO_DATA_PATHS','WORKER_PARTICIPATION']
for n,name in enumerate(names,1):
    section='## W2-'+sections[n].split('## Что передать сборщику')[0]
    ids={1:['K001'],2:['K002','K007'],3:['K003','K007'],4:['K004','K008'],5:['K005'],6:['K006']}[n]
    kparts=[]
    for kid in ids:
        m=re.search(r'(?ms)^## '+kid+r'\b.*?(?=^## |\Z)',critic)
        if m:kparts.append(m.group())
    dest=f'_WORK/W2_{n:02d}_{name}.md'
    # Preserve the critic's exact requested output filename where different.
    m=re.search(r'\*\*Выход:\*\*\s+([^\s]+\.md)',section)
    if m:dest=m.group(1).rstrip('.')
    text=brief+f'''\n# Индивидуальное поручение второй волны W2-{n:02d}\n
Ты новый исследователь gpt-6.1-sol medium, fork_turns=none. Первая волна из восьми отдельных агентов завершена, независимый критик gpt-6.1-sol high со свежим контекстом прочитал все результаты и сформулировал K001–K008. Ты устраняешь конкретный пробел, не повторяешь общий обзор. Полные первичные данные первой волны доступны в _WORK/W1_*.md; текущие источники получай самостоятельно там, где этого требует вопрос, а локальное повторное чтение явно отличай. Не запускай агентов, не контактируй с людьми.\n
Твой единственный результат: {dest}; дополнительные материалы — _WORK/W2_{n:02d}_MATERIALS/. Общие итоговые файлы и чужие ветки не редактируй. Локальные ID W2-{n:02d}-Sxx, W2-{n:02d}-Fxx, собственные Q/E. Сохраняй результат по мере работы. Финальная передача: что установлено, какое решение меняется, результат по K-ID, остаток, путь.\n
''' + section+'\n# Исходные замечания критика, сохраняемые без переписывания истории\n'+'\n'.join(kparts)
    if n==4:
        text+='\nОтдельная обязательная часть K008 — внутреннее согласование метрик и денежных формул на маленьком условном примере. Это методическая иллюстрация, не новый эксперимент и не наблюдение по данным продукта. Имеющиеся достаточные основания W1 не ищи заново.\n'
    (w/f'PROMPT_W2_{n:02d}.md').write_text(text,encoding='utf-8')
with (w/'AGENT_PROMPTS.md').open('a',encoding='utf-8') as f:
    f.write('\n## Вторая волна по независимой критике\n\n')
    for n,name in enumerate(names,1):f.write(f'- [W2-{n:02d}: {name}](PROMPT_W2_{n:02d}.md)\n')
print('Saved six W2 prompts; priority queue 02,03,05 then01,04,06')
