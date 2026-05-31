---
name: mental-toolkit
description: Structured mental health self-management toolkit with three modes -- worry-time (timed structured worry processing), scenario (decision/risk scenario planning), track (daily anxiety check-in with pattern detection). Triggered by "/mental", "worry time", "scenario plan", "track anxiety", "check in", or any request for structured anxiety/worry processing. Saves all output to Obsidian vault for longitudinal analysis.
---

# Mental Toolkit

Structured self-management toolkit for anxiety, rumination, and worry processing. Three modes that map to therapeutic interventions discussed with therapist Vadim.

**Philosophy:** Transform unstructured rumination into documented, time-bounded, actionable thinking. Every invocation produces a vault artifact that builds longitudinal self-knowledge.

## Modes

Parse the first argument as mode. Default to `track` if no argument given.

| Mode | Trigger | Duration | Output |
|------|---------|----------|--------|
| `worry` | `/mental worry` | 15 min default | Structured worry log |
| `scenario` | `/mental scenario [topic]` | Open-ended | Decision tree document |
| `track` | `/mental track` or `/mental` | 2-3 min | Daily check-in entry |
| `review` | `/mental review [period]` | 5 min | Pattern analysis across entries |
| `dims` | `/mental dims` | 2 min | Log DIMs/SIMs (danger/safety signals) |

## Vault Configuration

All output goes to: `~/Brains/brain/mental-toolkit/`

Subdirectories:
- `worry-sessions/` -- worry time logs
- `scenarios/` -- scenario planning documents
- `check-ins/` -- daily tracking entries
- `reviews/` -- periodic pattern analyses

Link to existing vault notes using wikilinks: `[[Generalized Anxiety disorder (GAD)]]`, `[[Sertraline]]`, `[[Trail - Living a Calm Life]]`, etc.

## Mode 1: Worry Time (`worry`)

Implements structured worry time as recommended by Vadim (session #2, 2026-03-13). The key distinction: **this is intentional, time-bounded worry processing, not rumination.**

### Invocation

```
/mental worry              # default 15 min
/mental worry 10           # 10 min session
/mental worry финансы       # pre-seeded with topic
```

### Workflow

**Step 1: Frame the session**

Display:
```
Worry Time Session -- [date] [time]
Timer: [N] minutes

Rules:
- One worry at a time
- For each: what exactly am I afraid of?
- Rate probability (0-100%)
- What's the worst case? Can I survive it?
- Is there an action I can take? If yes, note it. If no, park it.

Starting. What's on your mind?
```

Use AskUserQuestion to get the first worry. Accept voice input (the user often dictates).

**Step 2: Process each worry**

For each worry the user raises:
1. Reflect it back in one sentence (validate, don't minimize)
2. Ask: "On a scale of 0-100%, how likely is this?"
3. Ask: "What's the worst realistic outcome?"
4. Ask: "Is there one concrete action you could take about this? Even a small one?"
5. Categorize into one of the known anxiety threads (see Reference section)
6. Ask: "Next worry, or done?"

Keep the pace brisk. Don't over-therapize. You are a structured container, not a therapist.

**Step 3: Close and save**

After timer or user says done:
- Summarize: N worries processed, categories hit, actions identified
- Save to vault (format below)
- Remind: "Worries documented. If one comes back later today, you can tell yourself: I already processed this at [time]."

### Output Format

```markdown
---
type: worry-session
date: 'YYYY-MM-DD'
time: 'HH:MM'
duration_minutes: N
worry_count: N
categories: [finance, immigration, family, health, work, identity, other]
actions_identified: N
mood_before: N
mood_after: N
linked_sessions: ['[[previous-session]]']
---

# Worry Time -- YYYY-MM-DD HH:MM

## Worries Processed

### 1. [Short title]
- **Category:** [category]
- **Description:** [user's words, lightly cleaned]
- **Probability:** N%
- **Worst case:** [one sentence]
- **Action:** [concrete action or "No action needed -- parked"]

### 2. [...]

## Session Summary
- Total worries: N
- Categories: [list]
- Actions to take: [bulleted list of actionable items only]
- Parked worries: [list of worries with no action needed]

## Pattern Notes
[If this is not the first session: note any recurring worries, changes in probability ratings, worries that resolved since last session]
```

## Mode 2: Scenario Planning (`scenario`)

Structured alternative to worry-spiral on specific decisions. Produces a referenceable document so you don't need to re-think the same decision.

### Invocation

```
/mental scenario мама виза          # specific topic
/mental scenario паспорт            # specific topic
/mental scenario                    # will ask for topic
```

### Workflow

**Step 1: Define the decision/risk**

Ask the user to state the situation in 2-3 sentences. If they go long, gently redirect: "Let me capture the core question first."

Extract:
- The decision or risk being evaluated
- Timeline (when does this need resolution?)
- Who else is involved?
- What are the constraints?

**Step 2: Map scenarios**

Generate 3-5 scenarios ranging from best to worst case. For each:
- Description (1-2 sentences)
- Estimated probability (ask user to validate)
- Impact if it happens (1-10 scale)
- What you control vs. what you don't
- Concrete preparation steps

Present scenarios to user, ask for corrections/additions.

**Step 3: Decision/action plan**

Based on the scenario map:
- What's the default path (what happens if you do nothing)?
- What's the recommended action?
- What's the trigger to revisit? (date, event, or condition)
- What information would change the analysis?

**Step 4: Save**

```markdown
---
type: scenario-plan
date: 'YYYY-MM-DD'
topic: "[topic]"
status: active
review_date: 'YYYY-MM-DD'
categories: [relevant categories]
---

# Scenario Plan: [Topic]

Created: [[YYYYMMDD]]
Review by: YYYY-MM-DD

## Situation
[2-3 sentences]

## Constraints
- [list]

## Scenarios

### Scenario 1: [Best case] -- P: N%
[description]
- **Impact:** N/10
- **I control:** [list]
- **I don't control:** [list]
- **Preparation:** [steps]

### Scenario 2-5: [...]

## Decision
- **Default path:** [what happens if I do nothing]
- **Recommended action:** [specific next step]
- **Revisit trigger:** [date or condition]
- **Information that would change this:** [what to watch for]

## Linked
- Related worries: [wikilinks to worry sessions mentioning this topic]
- Therapy notes: [wikilinks to relevant session summaries]
```

## Mode 3: Daily Check-in (`track`)

Quick daily pulse. Designed for minimal friction -- should take under 3 minutes. Can be triggered via Telegram bot or Claude Code voice.

### Invocation

```
/mental track              # interactive check-in
/mental track quick 4      # non-interactive: anxiety=4, no details
```

### Workflow -- Interactive

Ask these questions sequentially. Accept terse answers. Don't probe unless something stands out.

1. "Anxiety level right now, 1-10?"
2. "Dominant worry thread?" (offer the known categories, accept free text)
3. "Sleep last night -- rough hours and quality (good/ok/bad)?"
4. "Exercise today? (yes/no, what)"
5. "One word for your energy level?"
6. "Anything else to note?" (optional, skip if user says no)

### Workflow -- Quick

If invoked with `quick N`, skip all questions, just log the number with timestamp.

### Health Data Integration

Before asking sleep/exercise questions, check if Apple Health data is available:

```bash
# Check for recent health export
ls -la ~/Brains/brain/health-data/ 2>/dev/null
```

If health data files exist, read sleep and exercise data from there instead of asking. Mention: "Got your sleep/exercise from Apple Health."

### Output Format

Append to daily file `~/Brains/brain/mental-toolkit/check-ins/YYYY-MM.md` (one file per month, entries appended):

```markdown
## YYYY-MM-DD

| Metric | Value |
|--------|-------|
| Anxiety | N/10 |
| Dominant thread | [category] |
| Sleep | Nh, [quality] |
| Exercise | [yes/no, type] |
| Energy | [word] |
| Note | [optional] |
```

If this is the first entry of the month, create the file with header:

```markdown
---
type: anxiety-tracker
month: 'YYYY-MM'
---

# Mental Check-ins -- YYYY-MM
```

## Mode 4: Review (`review`)

Analyze patterns across check-ins and worry sessions.

### Invocation

```
/mental review              # last 7 days
/mental review month        # last 30 days
/mental review all          # everything available
```

### Workflow

1. Read all check-in entries and worry sessions for the period
2. Compute:
   - Average anxiety level, trend (rising/falling/stable)
   - Most frequent worry categories
   - Correlation: anxiety vs. sleep quality, anxiety vs. exercise
   - Recurring worries (same topic across multiple worry sessions)
   - Resolved worries (appeared before, didn't appear recently)
   - Actions identified vs. actions presumably taken
3. If therapy session summaries exist in the vault for this period, cross-reference themes

### Output

Save to `~/Brains/brain/mental-toolkit/reviews/YYYY-MM-DD-review.md`:

```markdown
---
type: mental-review
date: 'YYYY-MM-DD'
period: [description]
avg_anxiety: N
trend: [rising|falling|stable]
---

# Mental Review -- [period]

## Summary
- Entries analyzed: N check-ins, N worry sessions, N scenarios
- Average anxiety: N/10 (trend: [direction])
- Most active threads: [top 3 categories with counts]

## Patterns
[Narrative analysis of what stands out]

## Correlations
- Sleep vs. anxiety: [observation]
- Exercise vs. anxiety: [observation]
- Day-of-week patterns: [if any]

## Worry Evolution
- **Recurring:** [worries that keep coming back]
- **Resolved:** [worries that dropped off]
- **New:** [worries that appeared this period]
- **Escalating:** [worries with rising probability ratings]

## Therapy Alignment
[If session summaries found: how do tracked patterns relate to therapy themes?]

## Suggestions
[2-3 specific, actionable observations -- not advice, just patterns worth noting]
```

## Mode 5: DIMs/SIMs Log (`dims`)

Tracks Danger In Me / Safety In Me micro-signals. Introduced by Vadim in session #3 (2026-03-19). The idea: tiny things throughout the day either add a sense of safety or trigger threat mode. Tracking them builds awareness and enables intentional rebalancing.

### Invocation

```
/mental dims                     # interactive logging
/mental dims skateboard sim      # quick log: skateboard = safety signal
/mental dims news dim            # quick log: news = danger signal
```

### Workflow -- Interactive

Ask: "Notice anything in the last few hours that added safety or triggered threat? Even tiny things."

For each item:
1. What was it? (1 sentence)
2. DIM or SIM?
3. How strong? (1-3: subtle/moderate/strong)
4. Was it voluntary or involuntary?

### Workflow -- Quick

Parse `[thing] [dim|sim]` and log directly.

### Output

Append to `~/Brains/brain/mental-toolkit/check-ins/dims-YYYY-MM.md`:

```markdown
## YYYY-MM-DD HH:MM

| Signal | Type | Strength | Voluntary |
|--------|------|----------|-----------|
| [thing] | DIM/SIM | 1-3 | yes/no |
```

### Known SIMs (from session #3)
- Skateboarding / surf skate
- Workout place (visualization alone helps)
- Hanging upside down on bars
- Making music with parametric instruments
- Talking to Claude Code while skating
- Exercise in general

### Known DIMs (from session #3)
- Watching war/Iran/Ukraine videos
- Reading Meduza news
- Alexander-related content/mentions
- Retelling Alexander betrayal story
- Thinking about border control/deportation scenarios
- Mother's messages (unread)

---

## Reference: Known Anxiety Threads

These are the recurrent worry categories identified across therapy sessions (Vadim #1 2026-03-05, #2 2026-03-13, #3 2026-03-19):

| Thread | Description | Status |
|--------|-------------|--------|
| `finance` | Money running out, economic crisis, business revenue | Active |
| `immigration` | VNZh/PMZh timeline, passport renewal, statelessness risk | Active |
| `family-mother` | Mother's visa plans, boundary management, invitation dilemma | Active |
| `family-ex` | Ex-wife interactions, divorce aftermath | Monitoring |
| `russia` | Travel risks, border control, political persecution, Telegram blocking | Active |
| `health` | Physical health, anxiety disorder itself, medication effects | Active, treated |
| `work` | Professional uncertainty, AI disruption, career direction | Active |
| `identity` | Narcissist narrative (Alexander), emigrant identity, "delayed life" | Background |
| `content` | Doom-scrolling, excessive news/politics consumption feeding anxiety | Active |
| `meaning` | Loss of spiritual framework, north star, "what am I doing with my life" | Background |

Update this table when new threads emerge or old ones resolve. The table lives in the skill file but should also be written to `~/Brains/brain/mental-toolkit/anxiety-threads.md` on first run.

## Behavioral Notes

- User often dictates via voice (Wispr Flow or Claude Code voice). Accept messy input, don't ask for clarification on obvious transcription errors.
- Russian is the primary language for emotional content. Accept Russian input, respond in whatever language the user is using.
- Don't be clinical. Don't diagnose. Don't say "I'm not a therapist." Just be a structured container.
- The user takes Sertraline (started ~early March 2026). Don't comment on medication unless asked.
- The user has a therapist (Vadim). Don't compete with or replace therapy. This tool is for *between-session* structured processing.
- If the user starts spiraling during worry time (going deeper into one topic without structure), gently redirect: "Let me capture what you've said so far. [summary]. Next worry, or action on this one?"
- Keep worry time sessions tight. The timer matters. When time is up, close the session even if there are more worries -- "We can do another session later."

## Integration Points

- **wispr-analytics**: Cross-reference dictation patterns (mental mode) with check-in data
- **coaching-session-summarizer**: Therapy session summaries provide context for review mode
- **calendar-sync**: Calendar density can be a stress signal
- **granola**: Therapy session transcripts feed the reference data
- **trail-checkin**: Trail "Living a Calm Life" is the overarching personal project this supports
