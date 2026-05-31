# DEMO SCRIPT — что показывать в терминале (Claude Code / Codex)

Презентерский ранбук для живой части. Всё на **синтетических** данных. Шрифт терминала 22–28pt.
Параллельно открыта доска (QR на первом слайде). Если терминал буксует — открываешь
соответствующий файл из `reference-outputs/` и продолжаешь.

## Соответствие слайдам

| Демо | Слайд(ы) на доске |
|---|---|
| 1. Анонимизация | «Анонимизация: до облака» (виджет статичный; терминал — живой) |
| 2. Разбор + аудит | «Живой разбор одной сессии» + «Аудит вывода» |
| 3. Массив + ключ | «Главное: паттерн через массив» + «Проверка по ключу» |
| 3б. Избегание / ДЗ / change talk | одноимённые слайды (board-driven) |
| 4. Три линзы | «ACT» + «Психодинамика» |
| 5. Самосупервизия | «Самопроверка протокола» |

## Pre-flight (до сцены)
- [ ] `cd ~/ai_projects/psychodemia-2026` — чистый клон, только синтетика.
- [ ] `.claudeignore` на месте; есть `demo/green_anon_reviewed/` и `demo/red_raw_local_only/` (пустая).
- [ ] Локальные модели скачаны заранее: `ollama pull qwen2.5:3b` (и `python -m spacy download ru_core_news_lg`).
- [ ] `OPENROUTER_API_KEY` в env (для доски). Один прогон каждого демо сделан заранее.
- [ ] НИКОГДА на сцене: установка пакетов, скачивание весов, логин, `--layers` со всеми тремя на 16 ГБ.

## Запуск
```bash
cd ~/ai_projects/psychodemia-2026
claude                 # или: codex
```

---

## Демо 1 — Анонимизация ЛОКАЛЬНО (≈6 мин) · «данные не уходят»
**Мысль:** локальные инструменты ≠ локальный инференс. Здесь инференс реально локальный.
> Слайд «Анонимизация: до облака» — статичный показ before/after. Терминал здесь — **живая**
> версия (реальная локальная модель). Это и есть доказательство «данные не уходят».

**Терминал (реальный локальный прогон):**
```bash
# показать, что агент видит ТОЛЬКО зелёную папку
cat .claudeignore
# локальная анонимизация русской сессии (Natasha + локальная LLM, без облака)
python3 skills/session-anonymizer/scripts/anonymize.py sessions-ru/client-a/session-01.md --layers natasha,ollama
```
Показать: поймало имена/город/препарат. Затем **ручная проверка квази-идентификаторов**
(промпт 2): «маркетолог + Яндекс + конкретный начальник» — связка деанонимизирует.
→ положить проверенный текст в `demo/green_anon_reviewed/`.

**Fallback:** `reference-outputs/01-anonymization.md`, `02-quasi-identifiers.md`.

---

## Демо 2 — Разбор одной сессии + аудит вывода (≈8 мин)
**Claude Code** — навык или промпт:
```
# вариант с навыком:
Используй навык cbt-session-analysis на demo/green_anon_reviewed/session-01-anon.md
# вариант с промптом: вставить промпт 3 (DoT) из prompts/PROMPTS.md
```
Показать обязательную схему: Доказательство → Интерпретация → Альтернатива → Уверенность
(словами) → Действие → Граница. Затем **аудит вывода** (промпт 4): supported / inferred /
unsupported — снять необоснованные утверждения.

**Codex (тот же навык, портируемо):**
```bash
codex exec --skip-git-repo-check --sandbox read-only \
  "Read skills/cbt-session-analysis/SKILL.md and apply it to demo/green_anon_reviewed/session-01-anon.md. Output in Russian."
```

**Fallback:** `reference-outputs/03-dot-analysis.md`, `04-output-audit.md`.

---

## Демо 3 — Паттерн через МАССИВ сессий (≈8 мин) · главный момент
```
Используй навык multi-session-patterns на папке sessions-ru/client-a/ (сессии 01–05)
```
Показать таблицу тренда: катастрофизация ↓, чтение мыслей ↑ (замещение), пробелы в ДЗ, тема
«отец». Затем **проверка по ключу** — открыть `sessions-ru/client-a/ANSWER-KEY.md`: один точный
результат, один пропуск, один спорный вывод (см. `reference-outputs/ground-truth-check.md`).

**Fallback:** `reference-outputs/05-multisession-trend.md`.

---

## Демо 3б (опц.) — избегание / ДЗ / change talk (board-driven)

Эти три — отдельные виджеты на доске (участники запускают сами; можно кликнуть на экране):
- **Избегание** — `avoidance` / `marina-all` (тема «отец»).
- **Домашние задания** — `homework` / `marina-all` (два пропуска проверки).
- **Change talk / sustain talk** — `changetalk` / `igor-all` (sustain → change через сессии).

В терминале избегание + ДЗ покрывает навык `multi-session-patterns` на `sessions-ru/client-a/`.
Change talk отдельным навыком не покрыт — показывай на доске или открой
`reference-outputs/10-change-sustain-talk.md`.

## Демо 4 (опц.) — Три линзы, один корпус (≈5 мин)
Тот же массив, другая модальность:
```
Используй навык act-lens на sessions-ru/client-a/         # ACT: towards/away, гибкость
Используй навык psychodynamic-lens на sessions-ru/client-a/  # CCRT, защиты — низкая уверенность
```
Подчеркнуть: ACT/психодинамика — экспериментально, только гипотезы для супервизии.
**Fallback:** `reference-outputs/act-marina.md`, `psychodynamic-marina.md`.

---

## Демо 5 (опц.) — Самосупервизия + свои данные (≈4 мин)
```
Используй навык cbt-supervision на sessions-ru/client-b/session-02.md   # X/10 + 5 вопросов супервизии
Используй навык synthetic-session-generator                            # сделать свои безопасные тест-данные
```

---

## Как вызывать навыки
- **Claude Code:** навыки в `~/.claude/skills/` → «используй навык <name> на <файл>» (или Skill-инструмент).
- **Codex:** навыки в `~/.agents/skills/` → `codex exec "Read skills/<name>/SKILL.md and apply it to <файл>"`.
- Установка пакета навыков: см. `skills/INDEX.md` (копирование/симлинк в обе папки).

## Жёсткие правила сцены
Только зелёная папка. Никогда не открывать `demo/red_raw_local_only/`. Если живой запуск >20с —
открыть `reference-outputs/`. Никаких установок/логинов/скачиваний весов вживую.
Отсутствие флага AI ничего не значит. Оценка риска — только человек.
