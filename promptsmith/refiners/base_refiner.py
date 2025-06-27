"""
Base Refiner module for iterative text improvement.
"""

import dspy


class Refiner(dspy.Signature):
    """
    You are an expert editor improving text based on specific feedback.
    
    Your task is to make minimal changes to address the feedback while preserving
    the original meaning and style. Focus only on the specific issue mentioned in the feedback.
    
    For each change you make:
    1. Explain what you changed and why
    2. Keep the explanation concise but specific
    3. Reference specific parts of the feedback you're addressing
    
    Return your reasoning and the refined output.
    """
    original_text: str = dspy.InputField(desc="The original input text.")
    current_output: str = dspy.InputField(desc="The current version to refine.")
    task_type: str = dspy.InputField(desc="Type of task (e.g., 'bulletize', 'restructure').")
    feedback_type: str = dspy.InputField(desc="Type of feedback (e.g., 'structure', 'coverage').")
    feedback: str = dspy.InputField(desc="Specific feedback to address.")
    
    reasoning: str = dspy.OutputField(desc="Explanation of the changes made to address the feedback.")
    refined_output: str = dspy.OutputField(desc="The improved output after addressing the feedback.")
