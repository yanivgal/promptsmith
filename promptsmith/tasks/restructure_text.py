import dspy

class RestructureText(dspy.Signature):
    """
    You are a text restructuring expert.

    Your task is to take long, dense text and rewrite it in the style of a clear and engaging blog post.

    Instructions:
    1. Start with a clear and informative title.
    2. Write a short introductory paragraph that summarizes the main idea.
    3. Break the content into logically grouped sections, each with a meaningful subheading.
    4. Use natural, human language with a smooth narrative flow between sections.
    5. Simplify technical terms and dense phrasing where possible, but do not change the original meaning.
    6. End with a brief concluding paragraph that highlights the key takeaway.
    7. Do not include images, visual references, or personal opinions.

    Be faithful to the original content. Do not add or invent new information.

    Return only the restructured version, including the title, subheadings, and clean paragraphs.
    """
    input_text: str = dspy.InputField(desc="The original long text.")
    output_text: str = dspy.OutputField(desc="The restructured text with a title, intro, and clean paragraphs.")
