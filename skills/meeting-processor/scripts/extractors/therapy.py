"""
Therapy session processor - extracts CBT/therapy-specific information
"""

import os
import json
import sys
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent.parent))
from interactive import generate_questions_therapy, apply_answers_therapy


def process(transcript_content, mode='interactive', user_answers=None):
    """
    Process therapy session transcript.

    Args:
        transcript_content: The transcript text
        mode: 'interactive' or 'batch'
        user_answers: Dict of answers from interactive mode

    Returns:
        str: Formatted markdown analysis
    """

    client = OpenAI(
        api_key=os.environ.get('CEREBRAS_API_KEY'),
        base_url="https://api.cerebras.ai/v1"
    )

    prompt = f"""Analyze this therapy session transcript and extract:

1. **Therapeutic Insights** - Key realizations, breakthroughs, pattern recognitions (3-5 items)
   - What did the client discover about themselves?
   - Any cognitive distortions identified?

2. **Techniques Used** - Therapeutic methods employed during session
   - e.g. CBT, behavioral experiments, cognitive restructuring, metacognitive therapy, exposure, etc.
   - Include any specific frameworks or models referenced

3. **Homework / Between-Session Tasks** - Assignments or experiments
   - Format: Task description [urgency: high/medium/low]

4. **Progress Markers** - What improved since last session, positive changes noted

5. **Medication Discussion** (if any)
   - Current medication, dosage, side effects, adjustments

6. **Session Themes** - Core emotional/psychological themes (2-4)

7. **Emotional Arc** - How the client's emotional state shifted during session

8. **Follow-up**
   - Next session scheduled? When?

Return as JSON:
{{
  "insights": ["..."],
  "techniques": ["..."],
  "homework": [
    {{"task": "...", "urgency": "high/medium/low"}}
  ],
  "progress_markers": ["..."],
  "medication": {{
    "discussed": true/false,
    "current": "medication name and dosage or null",
    "side_effects": ["... or empty"],
    "adjustments": "any changes or null"
  }},
  "themes": ["..."],
  "emotional_arc": "...",
  "followup": {{"scheduled": true/false, "date": "YYYY-MM-DD HH:MM timezone or null"}},
  "session_quality": {{
    "engagement": "high/medium/low",
    "depth": "high/medium/low",
    "therapeutic_alliance": "strong/adequate/strained",
    "sentiment": "positive/neutral/negative",
    "sentiment_reason": "..."
  }}
}}

Transcript:
{transcript_content}
"""

    response = client.chat.completions.create(
        model="qwen-3-235b-a22b-instruct-2507",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.choices[0].message.content.strip()

    # Parse JSON response
    try:
        if '```json' in result_text:
            result_text = result_text.split('```json')[1].split('```')[0].strip()
        elif '```' in result_text:
            result_text = result_text.split('```')[1].split('```')[0].strip()

        data = json.loads(result_text)
    except json.JSONDecodeError:
        return f"**Error:** Could not parse analysis\n\n```\n{result_text}\n```"

    # Interactive mode: apply user answers if provided
    if mode == 'interactive' and user_answers:
        data = apply_answers_therapy(data, user_answers)

    # Interactive mode: check if questions needed
    if mode == 'interactive' and not user_answers:
        questions = generate_questions_therapy(data)
        if questions:
            return {
                'needs_interaction': True,
                'questions': questions,
                'partial_data': data
            }

    # Format output
    output = []

    output.append("### Type")
    output.append("Therapy Session\n")

    # Therapeutic Insights
    if data.get('insights'):
        output.append("### Therapeutic Insights")
        for insight in data['insights']:
            output.append(f"- {insight}")
        output.append("")

    # Techniques Used
    if data.get('techniques'):
        output.append("### Techniques Used")
        for technique in data['techniques']:
            output.append(f"- {technique}")
        output.append("")

    # Homework
    if data.get('homework'):
        output.append("### Homework / Between-Session Tasks")
        for item in data['homework']:
            urgency = f" [{item['urgency']}]" if item.get('urgency') else ""
            output.append(f"- [ ] {item['task']}{urgency}")
        output.append("")

    # Progress Markers
    if data.get('progress_markers'):
        output.append("### Progress Markers")
        for marker in data['progress_markers']:
            output.append(f"- {marker}")
        output.append("")

    # Medication
    medication = data.get('medication', {})
    if medication.get('discussed'):
        output.append("### Medication")
        if medication.get('current'):
            output.append(f"**Current:** {medication['current']}")
        if medication.get('side_effects'):
            output.append("**Side effects:** " + ", ".join(medication['side_effects']))
        if medication.get('adjustments'):
            output.append(f"**Adjustments:** {medication['adjustments']}")
        output.append("")

    # Themes
    if data.get('themes'):
        output.append("### Session Themes")
        for theme in data['themes']:
            output.append(f"- {theme}")
        output.append("")

    # Emotional Arc
    if data.get('emotional_arc'):
        output.append("### Emotional Arc")
        output.append(data['emotional_arc'])
        output.append("")

    # Follow-up
    if data.get('followup', {}).get('scheduled'):
        output.append("### Follow-up")
        output.append(f"Next session: {data['followup']['date']}\n")

    # Session Quality
    quality = data.get('session_quality', {})
    if quality:
        output.append("### Session Quality")
        output.append(f"**Engagement:** {quality.get('engagement', 'unknown').capitalize()}")
        output.append(f"**Depth:** {quality.get('depth', 'unknown').capitalize()}")
        output.append(f"**Therapeutic Alliance:** {quality.get('therapeutic_alliance', 'unknown').capitalize()}")
        sentiment = quality.get('sentiment', 'neutral').capitalize()
        reason = quality.get('sentiment_reason', '')
        output.append(f"**Sentiment:** {sentiment} - {reason}")

    return '\n'.join(output)
