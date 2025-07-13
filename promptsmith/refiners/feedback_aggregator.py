import dspy

class FeedbackAggregator(dspy.Signature):
    """
    You are an expert summarizer combining multiple feedbacks into one clear, actionable message.
    
    Your job is to merge all feedbacks into a concise note that helps a writer improve their output.
    Focus ONLY on issues, problems, and areas that need improvement.
    
    CRITICAL: You must ONLY include feedback about problems, issues, and things that need to be changed.
    DO NOT include ANY positive feedback, praise, or statements about what is working well.
    
    Guidelines:
    1. Remove repetition or conflicting advice
    2. Prioritize clarity and usefulness
    3. Keep it focused and constructive
    4. ONLY include feedback about what needs to be changed or improved
    5. DO NOT include positive feedback or praise
    6. Present issues as clear, actionable bullet points
    7. If a judge's feedback contains both positive and negative comments, extract ONLY the negative parts
    8. Start each point with action words like "Fix", "Add", "Remove", "Change", "Improve", etc.

    Do not suggest improvements yourself — only summarize the feedback as-is.
    """
    original_text: str = dspy.InputField(desc="The original input text.")
    current_output: str = dspy.InputField(desc="The output that was evaluated.")
    task_type: str = dspy.InputField(desc="The task type, e.g., 'bulletize'.")
    judges_feedback: list = dspy.InputField(desc="List of feedback strings from different judges.")

    combined_feedback: str = dspy.OutputField(desc="Combined feedback from all judges into one message.")
