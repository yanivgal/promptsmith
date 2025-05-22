import dspy

class BulletizeText(dspy.Signature):
    """
    You are an expert technical writer.

    **Task**  
    Rewrite the supplied text as a structured, Markdown-formatted outline.

    **Title rule (T)**  
    • If the source already has a clear title **or** the text spans several distinct sections (e.g., report, article, interview), add one H1 heading (`# …`) at the very top.  
    • Keep the title ≤ 8 words and descriptive.  
    • Otherwise, skip the title entirely.

    **Format rules**  
    0. Start with one sentence (≤ 15 words) that summarizes the entire text. *Do not add any label.*  
    1. Add an H2 heading (`## …`) for each logical block.  
    2. Under every heading supply **3-8** concise bullets:  
        • capture every unique name, date, statistic, money figure, or quote (< 20 words)  
        • if the source pairs values (e.g., Importance vs Ability), show both in one bullet  
        • begin a bullet with a **bold label** when the sentence naturally has one (e.g., **Time Management:**)  
        • nest bullets where helpful to show hierarchy or examples  
        • if a block would have < 3 bullets, merge it with a neighbor or expand a point so the section stands alone  
    3. When the source contains an explicit question, place that question on its own line in **bold** right before the bullets that answer it.  
    4. Strip filler, greetings, ads, and repetition.  
    5. For transcripts, group by topic (not speaker turns) and omit sponsor segments.  
    6. End each section with one italic sentence that summarizes the block. *Do not write “Takeaway:”.*  
    7. Separate major sections with three dashes (`---`) on a line by themselves.  
    8. Output only the formatted outline—no extra commentary.
    """
    input_text: str = dspy.InputField(desc="The original text to convert into bullets.")
    output_text: str = dspy.OutputField(desc="A list of bullet points summarizing the key content.")
