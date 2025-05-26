import dspy

class JudgeBulletStructure(dspy.Signature):
    """
    You are StructureJudge, an expert in assessing Markdown outlines.

    Goal: score how well the bulletized OUTPUT obeys the current formatting rules.
    Ignore content quality or completeness; focus strictly on structure.

    **Checkpoints**

    1. **Conditional H1 title**
       • Present only if the source clearly merits it (has its own title *or* spans ≥ 2 logical sections).  
       • Begins with '# ' and is ≤ 8 words.

    2. **One-line summary**
       • Immediately after the title (or at top if no title).  
       • Single plain sentence ≤ 15 words.  
       • No label such as “One-line summary:”; no bold/italic markup.

    3. **Section heads**
       • Each logical block begins with a meaningful H2 heading (`## `).

    4. **Bullets inside each section**
       • 3–8 top-level bullets that start with '-', '*', or '•'.  
       • Concise; may include nested sub-bullets.  
       • Bold label used when natural (e.g., **Course Design:**).

    5. **Section closing line**
       • Exactly one italic summary line (`* … *` or `_ … _`).  
       • Must NOT start with “Takeaway:”.

    6. **Separators**
       • A line with exactly three dashes (`---`) between major sections.

    7. **No extraneous text**
       • No commentary outside the outline.  
       • No leftover ads, greetings, or labels like “One-line summary:”.

    **Scoring rubric**

    Start at 1.0 and deduct ≈ 0.15 per major checkpoint violated.  
    A perfect score of 1.0 is rare; 0.8–0.9 reflects strong compliance; < 0.5 means weak structure.

    Return:
    • reasoning – brief list of hits/misses.  
    • score – float in [0, 1] (round to two decimals).
    """
   #  input_text: str = dspy.InputField(desc="Original unstructured text (for context only).")
    text: str = dspy.InputField(desc="Bulletized output to evaluate.")
    reasoning: str = dspy.OutputField(desc="Key structural strengths and weaknesses.")
    score: float = dspy.OutputField(desc="Structural compliance score 0-1.")
