"""
Mentoring/lab session processor - extracts skill-transfer and accountability information
"""

import os
import json
import sys
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent.parent))
from interactive import generate_questions_mentoring, apply_answers_mentoring


def process(transcript_content, mode='interactive', user_answers=None):
    """
    Process mentoring/lab 1-on-1 session transcript.

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

    prompt = f"""Analyze this mentoring/lab 1-on-1 session transcript. This is a session between a mentor and a participant where the mentor teaches tools, workflows, and principles, reviews progress on previous tasks, and assigns new ones.

Extract:

1. **Key Ideas** - Numbered principles, insights, or aha-moments from the session (3-8 items)
   - These should be transferable ideas, not just "we talked about X"

2. **Progress Review** - Status of action items from previous sessions mentioned in the conversation
   - For each item: what was it, what's the status (done/in-progress/pending/not-started)
   - Only include items explicitly referenced in the conversation

3. **Tools & Demos** - Specific tools, workflows, apps, or techniques shown or discussed
   - Include the name and brief purpose

4. **Action Items** - New tasks for the participant, tiered by urgency:
   - "this_week" - do before next session
   - "next_call" - bring/prepare for next session
   - "when_ready" - longer-term, no deadline pressure

5. **Focus Areas** - The 2-4 areas the participant is currently developing

6. **Follow-up**
   - Next session scheduled? When?

Return as JSON:
{{
  "key_ideas": [
    {{"number": 1, "idea": "..."}}
  ],
  "progress_review": [
    {{"item": "...", "status": "done/in-progress/pending/not-started", "notes": "..."}}
  ],
  "tools_demos": [
    {{"name": "...", "purpose": "..."}}
  ],
  "action_items": {{
    "this_week": ["..."],
    "next_call": ["..."],
    "when_ready": ["..."]
  }},
  "focus_areas": ["..."],
  "followup": {{"scheduled": true/false, "date": "YYYY-MM-DD HH:MM timezone or null"}},
  "session_quality": {{
    "engagement": "high/medium/low",
    "progress_pace": "accelerating/steady/stalled",
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
        data = apply_answers_mentoring(data, user_answers)

    # Interactive mode: check if questions needed
    if mode == 'interactive' and not user_answers:
        questions = generate_questions_mentoring(data)
        if questions:
            return {
                'needs_interaction': True,
                'questions': questions,
                'partial_data': data
            }

    # Format output
    output = []

    output.append("### Type")
    output.append("Mentoring Session\n")

    # Key Ideas
    if data.get('key_ideas'):
        output.append("### Key Ideas")
        for item in data['key_ideas']:
            num = item.get('number', '')
            output.append(f"**#{num}** {item['idea']}")
        output.append("")

    # Progress Review
    if data.get('progress_review'):
        output.append("### Progress Review")
        status_icons = {
            'done': 'x',
            'in-progress': '/',
            'pending': ' ',
            'not-started': ' '
        }
        for item in data['progress_review']:
            status = item.get('status', 'pending')
            icon = status_icons.get(status, ' ')
            notes = f" -- {item['notes']}" if item.get('notes') else ""
            label = status.capitalize() if status != 'done' else 'Done'
            output.append(f"- [{icon}] {item['item']} ({label}){notes}")
        output.append("")

    # Tools & Demos
    if data.get('tools_demos'):
        output.append("### Tools & Demos")
        for tool in data['tools_demos']:
            output.append(f"- **{tool['name']}** -- {tool['purpose']}")
        output.append("")

    # Action Items
    actions = data.get('action_items', {})
    if any(actions.values()):
        output.append("### Action Items")

        if actions.get('this_week'):
            output.append("**This week:**")
            for item in actions['this_week']:
                output.append(f"- [ ] {item}")

        if actions.get('next_call'):
            output.append("**Before next call:**")
            for item in actions['next_call']:
                output.append(f"- [ ] {item}")

        if actions.get('when_ready'):
            output.append("**When ready:**")
            for item in actions['when_ready']:
                output.append(f"- [ ] {item}")
        output.append("")

    # Focus Areas
    if data.get('focus_areas'):
        output.append("### Focus Areas")
        for area in data['focus_areas']:
            output.append(f"- {area}")
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
        output.append(f"**Progress Pace:** {quality.get('progress_pace', 'unknown').capitalize()}")
        sentiment = quality.get('sentiment', 'neutral').capitalize()
        reason = quality.get('sentiment_reason', '')
        output.append(f"**Sentiment:** {sentiment} - {reason}")

    return '\n'.join(output)
