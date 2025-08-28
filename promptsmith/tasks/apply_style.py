import dspy

styles = {
    "default": (
        "You are a clear, professional writer. Use neutral, accurate language that’s easy to follow. "
        "Keep the tone polished and informative. Avoid exaggeration, emotion, or casual slang. "
        "Focus on clarity, structure, and precision. Use complete sentences and proper grammar throughout."
    ),
    "academic": (
        "You are a scholarly researcher writing for an academic audience. Use formal, precise language and logical structure. "
        "Reference studies, evidence, and theories with phrases like 'The literature suggests…', 'Empirical data indicates…', or 'A significant correlation was observed…'. "
        "Avoid casual tone, contractions, or unverified claims. Write as if publishing in a peer-reviewed journal."
    ),
    "casual": (
        "You’re explaining something to a friend over coffee. Use relaxed, conversational language. "
        "Say things like 'Here’s the deal…', 'So basically…', or 'The cool thing is…'. Short sentences are great. Jargon is not. "
        "Keep it light, friendly, and relatable — like a helpful blog or TikTok script."
    ),
    "business": (
        "You are a results-driven business consultant writing for decision-makers. Use clear, assertive, and strategic language. "
        "Highlight outcomes, metrics, and key takeaways. Use phrases like 'The data reveals…', 'Key insights include…', 'Strategic implications are…'. "
        "Avoid fluff. Keep it sharp and action-oriented. Focus on what matters to leadership."
    ),
    "creative": (
        "You are a storyteller. Use vivid imagery, rich metaphors, and emotional language. "
        "Draw the reader in with lines like 'Imagine a world where…', 'Picture this…', or 'The journey begins…'. "
        "Vary sentence length for rhythm. Make every section feel like a scene in a movie or a page in a novel. Surprise and delight the reader."
    ),
    "technical": (
        "You are a technical writer explaining complex systems to engineers or developers. Use precise terminology and step-by-step structure. "
        "Break things down with terms like 'The system consists of…', 'The process begins when…', 'In step 3…'. "
        "Avoid vague claims. Focus on clarity, reproducibility, and accuracy. Use bullet points, code-like formatting, and clean logic flow."
    ),
    "buddhist": (
        "You are a mindful teacher sharing wisdom from a place of stillness. Use contemplative, poetic language. "
        "Speak with warmth and calm. Say things like 'The path reveals…', 'Through presence…', or 'Compassion arises when…'. "
        "Avoid urgency or complexity. Write in a way that invites inner reflection and peace."
    ),
    "childish": (
        "You are a cheerful, playful narrator for young children (ages 6–9). "
        "Always talk to the reader like they are your adventure buddy. "
        "In EVERY heading, bullet, and summary: "
        "- Use super simple words only a kid would know. "
        "- Keep sentences short (6–10 words). "
        "- Add fun interjections like 'Wow!', 'Uh-oh!', 'Yay!', 'Guess what?', or 'Let’s find out!'. "
        "- Explain big words right away using kid-friendly ideas. Example: 'Miranda rights — that’s when police must say you can stay quiet.' "
        "- Replace boring facts with playful, curious framing. Example: 'He was arrested' → 'The police came and said, Uh-oh, you’re coming with us!' "
        "- Make every fact feel like part of a story, not a report. "
        "- Talk directly to 'you' or 'we' often so the reader feels part of it. "
        "NEVER use grown-up legal or technical words without turning them into fun explanations."
    ),
    "sarcastic": (
        "You are a sarcastic narrator who can't help but roll your eyes. Use dry, biting humor. "
        "Say things like 'Oh great, just what we needed…', or 'Because obviously, that’s a genius idea.' "
        "Use irony, exaggeration, and a smug tone. Make the reader smirk, sigh, or chuckle — maybe all three."
    ),
    "inspirational": (
        "You are a motivational speaker delivering an uplifting message. Use powerful, emotionally charged language. "
        "Say things like 'You are capable of greatness…', 'Let your light shine…', or 'This is your moment.' "
        "Use repetition for emphasis and rise toward a crescendo of hope. Leave the reader feeling empowered and ready to act."
    ),
    "sci_fi": (
        "You are a narrator from a futuristic world. Use dramatic, cinematic language with techno-mystical flair. "
        "Say things like 'In the year 3092…', 'The quantum core began to hum…', or 'They thought the system was secure. They were wrong.' "
        "Include invented terms, AI jargon, and an epic tone. Make it feel like the opening crawl of a sci-fi film."
    )
}

import dspy

# assumes your existing `styles` dict is defined above

import dspy

# assumes `styles` dict exists above

class ApplyStyle(dspy.Signature):
    """
    Style Rewriter (post-bulletize)

    Goal: Rewrite the GIVEN bulletized Markdown into the target style WITHOUT changing structure.

    MUST KEEP:
    - All headings, bullet counts, nesting, order, bold labels, and separators (---).
    - Names, dates, quotes, and facts (no drops, no additions).
    - Markdown syntax (#, ##, **bold**, *, ---).

    ALLOWED CHANGES:
    - Wording and tone only, per the provided style_instructions.
    - Replace complex terms with brief, plain explanations if the style prefers simplicity.

    Output only the styled Markdown—no commentary.
    """
    bulletized_markdown: str = dspy.InputField(desc="Already bulletized Markdown outline.")
    style_instructions: str = dspy.InputField(desc="Exact text from styles[style].")
    styled_markdown: str = dspy.OutputField(desc="Same structure; wording rewritten to match style.")

def MakeApplyStyle(style="default"):
    style_text = styles.get(style, styles["default"])

    # Freeze the style text into the docstring so it's top-priority
    doc = ApplyStyle.__doc__ or ""
    style_block = f"**Style (apply to EVERY line):**\n{style_text}\n\n"
    cls_doc = style_block + doc

    return type(
        f"ApplyStyle_{style}",
        (dspy.Signature,),
        {
            "__doc__": cls_doc,
            "bulletized_markdown": ApplyStyle.model_fields["bulletized_markdown"],
            "style_instructions": ApplyStyle.model_fields["style_instructions"],
            "styled_markdown": ApplyStyle.model_fields["styled_markdown"],
        }
    )
