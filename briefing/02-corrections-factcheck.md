# Audit & Fact-Check — required corrections before the masterclass

Verified against primary sources by independent research agents (2026-05-29). Grouped most-
concerning first. **Every item here is a change to make in the deck/narration.** Audience is
science-oriented; uncorrected errors are the top reputational risk.

---

## A. The anonymization tool — "OpenAI Privacy Filter"

**It is REAL** (verified via GitHub org API + HuggingFace API, not just web search):
- `github.com/openai/privacy-filter` — genuine OpenAI org, Apache-2.0, ~2.3k stars, created 2026-04-17.
- `huggingface.co/openai/privacy-filter` — `author: openai`, `token-classification`, Apache-2.0,
  ~302k downloads, **~1.4–1.5B total params**.
- Model card PDF: https://cdn.openai.com/pdf/c66281ed-b638-456a-8ce1-97e9f5264a90/OpenAI-Privacy-Filter-Model-Card.pdf

**Deck errors to fix:**
1. **Date:** released **April 2026**, not "April 2025." (Off by a year.)
2. **Install:** the deck's `pip install 'opf @ git+…'` is wrong. **There is no `opf` package on
   PyPI.** Real method: `git clone … && pip install -e .` (the `opf` CLI exists only after the
   editable install; weights auto-download). README also shows a plain
   `transformers.pipeline("token-classification", "openai/privacy-filter")` path.
3. **"50M active via LoRA":** wrong — it's a **MoE active-parameter count** (128 experts, top-4
   routing), not LoRA.
4. **The 8-category list is wrong.** Actual labels (from `config.json id2label`):
   `private_person, private_address, private_email, private_phone, private_url, private_date,
   account_number, secret`. **No ORG, no generic LOCATION, no OTHER, no ID_NUM.** (The deck's
   example *tags* happen to match real label names; the summarized list does not.)
5. **Russian support is weak — this is the dealbreaker.** Model card: "Primarily English…
   performance may drop on non-Latin scripts." Community reports it largely ignores Cyrillic.
   For a privacy demo, silent **false negatives = leaked PII** = worst case.

**Resolution (already adopted):** demo OpenAI Privacy Filter on **English** + show real evals;
anonymize the **Russian** transcripts with **Microsoft Presidio + spaCy `ru_core_news_lg`**
(genuinely multilingual, local, OSS) plus a regex safety net for emails/phones/dates. State on
stage that the OpenAI model is English-first. Treat any single model as "a data-minimization aid,
not an anonymization guarantee" (the model card's own words).

---

## B. MISATTRIBUTED / FABRICATED — fix or remove

### B1. "Garland et al., 2016 — 78% self-rated vs 42% objective adherence"
**Fabricated numbers + wrong author.** Real study: **Hogue, Dauber, Lichvar, Bobek & Henderson
(2015)**, *Admin. Policy Ment. Health* 42(2):229–243. Finding (therapists overestimate adherence
vs observers) is real and significant, but reported as **Likert means** (e.g., 2.18 vs 1.8 on a
5-pt scale), **not percentages**. → Replace with: "Therapists systematically rate their own
protocol adherence higher than independent observers (Hogue et al., 2015)." Drop 78/42.
Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC4763603/

### B2. "COMPASS approach" for therapeutic alliance
**Not a clinical framework.** "COMPASS" is either (a) a 2024 **NLP method** to infer working
alliance from transcripts (Lin et al., arXiv:2402.14701, *Transl. Psychiatry* 2025), or (b) a
commercial measurement-based-care product. → For alliance indicators cite the **Working Alliance
Inventory (Horvath & Greenberg)** / **Bordin's** bond–tasks–goals model. Cite COMPASS only as an
AI method, correctly.

### B3. "Hatcher et al., 2012 — clients don't change behavior when recorded"
**Unverified.** No such 2012 publication located making that claim. → Either find the exact
reference or replace with the **2025 camera-reactivity systematic review/meta-analysis**
(Springer, *Systematic Reviews*): https://link.springer.com/article/10.1186/s13643-025-03055-z

---

## C. PARTIALLY CORRECT — numbers/attribution need fixing

### C1. Russia 152-ФЗ fines (major increases took effect **30 May 2025**, КоАП 13.11)
- No-consent processing: **up to 700,000 ₽** for legal entities (deck's "300,000" is the
  failure-to-notify / smaller tier).
- Special-category **data leak: 10–15 million ₽** (deck's "500,000" is false/severely understated).
- Localization violation: **1–6M first time; 6–18M on repeat** (deck's flat "18M" is repeat-only;
  in force since 1 July 2025).
- Repeat **leaks** → **turnover fines 1–3% of annual revenue** (floor ~20–25M, cap 500M ₽), not a
  flat ×2.
- Sources: https://www.consultant.ru/legalnews/28492/ · https://data-sec.ru/personal-data/fines/
- ✅ Keep: "sending a session transcript to ChatGPT = cross-border transfer of special-category PD"
  — legally sound framing.

### C2. APA concern percentages
From the **APA 2025 Practitioner Pulse Survey** (the real source, see D1):
- Data privacy **67%** ✅; algorithmic bias **63%** ✅.
- Inaccuracy/hallucinations: **60%** (deck says 51% — **use 60%**).
- Job-loss/replacement: **38%** (deck says 34% — **use 38%**).
- "Ethics 48%" and "don't know how to start 29%" — **not found in the report**; remove or mark unverified.

### C3. Distortion list attribution
Accurately named, but **not all Beck.** Beck (1976): arbitrary inference, selective abstraction,
overgeneralization, magnification/minimization, personalization, dichotomous thinking. **Burns
(1980)** popularized: mind reading, fortune telling, mental filter, should statements, discounting
the positive, emotional reasoning, labeling. → Attribute as **"Beck (1976) and Burns (1980)."**

### C4. "10–15 minutes" camera habituation
Loosely cited. Behavioral-observation literature usually discards the **first 3–5 min**. → Say
"reactivity diminishes after an initial adaptation period" and cite the 2025 meta-analysis (B3).

---

## D. CONFIRMED (use with confidence; minor tweaks noted)

- **D1. APA 2025 Practitioner Pulse Survey** — "AI in the Therapist's Office," n=1,742, fielded
  Sep 2025, released Dec 2025. **56% used AI in past 12 mo** (up from 29% in 2024); **8% used AI
  for clinical diagnosis** (of AI users). Frame the "48-pt gap" precisely as *general use vs
  clinical-diagnosis use*. https://www.apa.org/news/press/releases/2025/12/psychologists-ai-use-concerns
- **D2. GDPR Art. 9** (health = special category; explicit consent; DPIA), **EU AI Act** (much
  healthcare AI = high-risk, phasing 2026–27), max fine **€20M or 4% global turnover**. ✅
- **D3. HIPAA** — psychotherapy notes specially protected ✅; OpenAI/Anthropic sign BAAs only for
  API/Enterprise, not consumer ChatGPT/Claude ✅; **2026 Tier-4 annual cap ≈ $2.19M** (update from
  "$1.9M"). https://www.hipaajournal.com/hipaa-violation-fines/
- **D4. Diagnosis of Thought (DoT)** — Chen, Lu & Wang (2023), **arXiv:2310.07146**. 3 steps:
  (1) Subjectivity assessment, (2) Contrastive reasoning, (3) **Schema analysis** — **not
  "classification"** (deck step 3 is mislabeled; schema analysis then maps to distortion types).
  English-only.
- **D5. Datasets** (all real, **English-only**): **MentalChat16K** (PennShenLab, arXiv 2503.13509);
  **CACTUS** — correct expansion is **"CBT-augmented Counseling Chat Corpus"** (not "Cognitive
  Automated CBT Training Using Simulations"), arXiv 2407.03103, EMNLP-F 2024; **CBT-Bench**
  (arXiv 2410.13218, NAACL 2025).
- **D6. BABCP** requires recorded sessions for CBT accreditation ✅ (CBP Accreditation Guidelines,
  Oct 2024).
- **D7. CTS-R** rates competence from recordings ✅ — but developed by **Blackburn et al. (2001)**
  (Newcastle), **not the Beck Institute** (original CTS was Young & Beck, 1980).
- **D8. Change talk / sustain talk** — **Miller & Rollnick** (correct order; deck reversed it).

---

## Edit checklist (paste into deck review)
1. opf: date → Apr 2026; install → `pip install -e .` (no PyPI `opf`); not LoRA; fix category list; English-only.
2. Garland/78–42 → Hogue et al. 2015, Likert means, no %.
3. COMPASS → WAI/Bordin (or COMPASS-as-NLP-method).
4. 152-ФЗ: 700k no-consent; 10–15M special-cat leak; 1–6M / 6–18M localization; turnover % on repeat.
5. APA concerns: inaccuracy 60%; replacement 38%; drop ethics-48 / start-29.
6. DoT step 3 → "schema analysis."
7. CACTUS → "CBT-augmented Counseling Chat Corpus."
8. HIPAA cap → ~$2.19M (2026).
9. CTS-R → Blackburn et al. 2001.
10. "Miller & Rollnick" order; distortions "Beck 1976 & Burns 1980."
11. Hatcher 2012 → verify or replace with 2025 meta-analysis.
