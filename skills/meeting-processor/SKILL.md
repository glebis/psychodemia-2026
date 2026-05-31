---
name: meeting-processor
description: This skill should be used when processing meeting transcripts to auto-detect meeting type (leadgen, partnership, coaching, therapy, mentoring, internal) and extract type-specific structured analysis. Triggers on "process meeting", "analyze meeting", "meeting summary", or after syncing new Fathom/Granola transcripts.
---

# Meeting Processor

Intelligent meeting transcript processor that auto-detects meeting type and applies type-specific extraction with optional interactive clarification.

## When to Use

- After syncing Fathom or Granola transcripts (`/fathom --today`, `/granola export`)
- When asked to process, analyze, or summarize a meeting transcript
- When a new meeting transcript appears in the vault root matching `YYYYMMDD-*.md`
- For therapy sessions (CBT, psychiatry), auto-detects and uses therapy-specific extraction

## Prerequisites

```bash
pip install openai pyyaml
```

Requires `CEREBRAS_API_KEY` environment variable (uses Cerebras API with llama-3.3-70b).

## Supported Meeting Types

| Type | Description | Key Extractions |
|------|-------------|-----------------|
| **leadgen** | Sales/business development calls | Commitments, pain points, budget, timeline, decision makers, deal stage, sentiment |
| **partnership** | Collaboration/partnership exploration | Opportunity overview, value proposition, strategic alignment, technical needs, fit assessment |
| **coaching** | Coaching/mentoring sessions | Insights, decisions, action items, themes, emotional arc, techniques, session quality |
| **therapy** | Psychotherapy/psychiatry sessions | Therapeutic insights, techniques, homework, medication, progress markers, emotional arc |
| **mentoring** | Mentoring/lab 1-on-1 sessions | Key ideas, progress review, tools & demos, tiered action items, focus areas |
| **internal** | Internal team meetings | Coming soon |

## Usage

### Interactive Mode (default)

Run the processor, which auto-detects meeting type and asks clarifying questions:

```bash
python3 ~/.claude/skills/meeting-processor/scripts/process.py <transcript-file> --mode interactive
```

**Interactive flow:**
1. Script analyzes transcript and detects meeting type
2. Extracts structured data via LLM
3. Identifies missing/ambiguous fields
4. Returns questions as JSON (exit code 2 signals interaction needed)
5. Parse the JSON between `__INTERACTIVE_QUESTIONS__` markers
6. Use AskUserQuestion to collect answers for each question
7. Save answers to a temp JSON file and re-run with `process_with_answers.py`

**Handling interactive questions:**

When the script exits with code 2, parse the output for questions JSON. Each question has:
- `question`: The question text
- `header`: Short label (used as answer key)
- `options`: Array of `{label, description}` for AskUserQuestion

After collecting answers, create two temp files:
- `questions.json` — the original questions context (includes `partial_data`, `meeting_type`, `transcript_file`)
- `answers.json` — map of `{header_lowercase: selected_label}`

Then run:
```bash
python3 ~/.claude/skills/meeting-processor/scripts/process_with_answers.py questions.json answers.json
```

### Batch Mode

Extract only high-confidence information without user interaction:

```bash
python3 ~/.claude/skills/meeting-processor/scripts/process.py <transcript-file> --mode batch
```

### Force Meeting Type

Skip auto-detection:

```bash
python3 ~/.claude/skills/meeting-processor/scripts/process.py <transcript-file> --type leadgen
python3 ~/.claude/skills/meeting-processor/scripts/process.py <transcript-file> --type partnership
```

## Output

Analysis is appended to the transcript file as a `## Meeting Analysis` section. Frontmatter is updated with `meeting_type`, `processed_date`, and `processing_mode`.

### Leadgen Output Structure

- **Commitments & Actions** — with deadlines and owners
- **Follow-up** — next meeting date if scheduled
- **Client Context** — pain points, budget, timeline, decision makers
- **Deal Assessment** — stage (cold/warm/hot), probability (1-5), blocker, sentiment

### Partnership Output Structure

- **Opportunity** — description and value proposition for both sides
- **Commitments & Actions** — with deadlines and owners
- **Follow-up** — next meeting date if scheduled
- **Partnership Context** — strategic alignment, technical needs, resources, challenges
- **Opportunity Assessment** — fit (strong/medium/weak), readiness, success factors, sentiment

### Therapy Output Structure

- **Therapeutic Insights** — key realizations, cognitive distortions identified
- **Techniques Used** — therapeutic methods and frameworks employed
- **Homework** — between-session tasks with urgency markers
- **Progress Markers** — improvements noted since last session
- **Medication** — current medication, side effects, adjustments (if discussed)
- **Session Themes** — core psychological themes
- **Emotional Arc** — emotional state shifts during session
- **Session Quality** — engagement, depth, therapeutic alliance, sentiment

## Step 2: Entity Extraction & People Updates

After the meeting analysis is complete (Step 1), run entity extraction and update People files.

### Entity types to extract

From the transcript, identify all mentioned entities across these types:

| Type | Vault location | Frontmatter `type:` | When to create/update |
|------|---------------|--------------------|-----------------------|
| **People** | `People/@Name.md` | `person` | Always — every named person except Gleb |
| **Companies** | `Companies/Name.md` | `company` | When a company is discussed substantively (not just mentioned in passing) |
| **Communities** | `Communities/Name.md` | `community` | When a community/group is discussed with specifics (size, purpose, membership) |
| **Projects** | Link to existing Trail or create stub | `project` | When a specific project is discussed with enough detail to merit a page |
| **Events** | `Events/YYYYMMDD Name.md` | `event` | When a specific conference/event is discussed with date + details |

**Skip extraction for:**
- Generic tool/product names mentioned in passing (e.g., "I use Notion")
- Concepts or ideas (capture these in the meeting analysis, not as entities)
- Gleb Kalinin himself

### How to update entity files

For each extracted entity of ANY type:

1. **Check if file exists** using Glob (check vault-wide, not just expected folder — entities may be in unexpected places)
2. **If exists** — update in compiled truth + timeline format:
   - Read the existing file
   - If it already has `## Compiled Truth` section — merge new facts into it (don't replace existing info unless contradicted)
   - If it doesn't have compiled truth format — restructure it into the format (preserve all existing content in timeline)
   - Append a new `### YYYY-MM-DD — {event title}` entry to the `## Timeline` section with:
     - 2-5 bullet points summarizing what was discussed
     - `Source: [[transcript-filename]]` link
   - Update `last_updated:` in frontmatter
3. **If doesn't exist** — create at the appropriate vault location with:
   - Frontmatter: aliases (English + Russian if bilingual), type, last_updated
   - `## Compiled Truth` with what's known from the transcript (2-5 lines)
   - `## Timeline` with the first entry from this meeting
4. **Cross-link** — if the entity relates to a person (e.g., "Darya is founder of Venturing Women"), update both entity files with `[[wikilinks]]` to each other

### Compiled Truth + Timeline format reference

```markdown
---
aliases: ["Name Surname", "Имя Фамилия"]
type: person
last_updated: YYYY-MM-DD
---

# Name Surname

## Compiled Truth
<!-- Agent rewrites this section when new info appears -->

[Current synthesis: who they are, current focus, relationship to Gleb, working style. 5-10 lines max.]

---

## Timeline
<!-- Append-only. Never edit entries below. Newest first. -->

### YYYY-MM-DD — Event title
- Key point 1
- Key point 2
- Key point 3
- Source: [[transcript-filename]]
```

### Rules

- **Never fabricate** — only use information explicitly stated in the transcript
- **Merge, don't overwrite** — if compiled truth already has a fact, don't remove it unless the transcript explicitly contradicts it
- **Timeline is append-only** — never edit or delete past entries
- **Skip Gleb Kalinin** — don't create/update a People file for the vault owner
- **Bilingual aliases** — if the person speaks Russian, include both English and Russian name forms
- **Link to source** — every timeline entry must reference the transcript file with `[[wikilink]]`

### Automation

When processing meetings in batch mode, entity extraction runs automatically after the meeting analysis. In interactive mode, it runs after the user has answered all clarifying questions.

To run entity extraction on an already-processed transcript:
```
Process the entities from [[YYYYMMDD-meeting-file]] and update People files
```

## Step 3: Auto-Link Prep Notes

After processing is complete (Steps 1-2), automatically link any matching meeting-prep notes to the session note. This replaces the need to manually run `/meeting-prep link`.

### How It Works

1. **Derive the meetings directory** from the processed session note's parent directory (do not hardcode paths).

2. **Extract session metadata** from the processed note:
   - `date` from frontmatter (YYYYMMDD format)
   - `participants` from frontmatter (list of names)
   - If no `participants` field, extract names from the transcript header or attendee list

3. **Search for matching prep notes**:
   ```bash
   find <MEETINGS_DIR> -name "YYYYMMDD-prep-*" -type f 2>/dev/null
   ```
   Where `YYYYMMDD` is the session date. The `prep` prefix matches the meeting-prep skill's default `prep_notes.prefix` from its `config.yaml`.

4. **Validate the match**: For each candidate prep note, read its frontmatter and confirm:
   - The `date` field matches the session date
   - The `participant` field matches one of the session's participants (fuzzy: check both full name and first name, case-insensitive)
   - The `session_note` field is empty (`""`) — skip already-linked prep notes

5. **Update both files** when a match is found:

   **In the prep note:**
   - Set `session_note: "[[session-note-filename]]"` (without `.md` extension)
   - Set `status: done`

   **In the session note:**
   - If a `## See also` section exists, add `- [[YYYYMMDD-prep-participant-slug]]` to it
   - Otherwise, append a new section at the end:
     ```markdown
     ## Prep Note
     - [[YYYYMMDD-prep-participant-slug]]
     ```
   - Never create duplicate links — check if the link already exists before adding

6. **Report** in the processing output:
   - Which prep notes were linked (prep filename + session filename)
   - Which prep notes were found but skipped (already linked)
   - If no prep note was found for this session, note it briefly (not an error)

### Rules

- Derive `MEETINGS_DIR` from the session note path, not from hardcoded values
- If the meeting-prep `config.yaml` is available at `~/.claude/skills/meeting-prep/config.yaml` or `~/ai_projects/claude-skills/meeting-prep/config.yaml`, read it to get the `prep_notes.prefix` (default: `prep`) and `prep_notes.type_tag` (default: `meeting-prep`)
- If config is unavailable, fall back to prefix `prep` and type tag `meeting-prep`
- This step is non-blocking: if it fails or finds no prep notes, processing still succeeds
- Log the link result but do not prompt the user for confirmation
