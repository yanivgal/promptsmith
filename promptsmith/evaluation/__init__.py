"""
Evaluation module for running and scoring tasks with multiple judges.

This module provides tools to:
1. Run a task on input text
2. Evaluate the output using multiple judges
3. Calculate combined scores with custom weights
4. Track evaluation results and reasoning

Example:
    from promptsmith.evaluation import TaskEvaluator, EvaluationResult
    from promptsmith.tasks.bulletize_text import BulletizeText
    from promptsmith.judges import JudgeBulletStructure, JudgeCoverage
    
    # Create an evaluator with weighted judges
    evaluator = TaskEvaluator(
        task=dspy.ChainOfThought(BulletizeText),
        judges={
            'structure': dspy.Predict(JudgeBulletStructure),
            'coverage': dspy.Predict(JudgeCoverage)
        },
        weights={'structure': 0.7, 'coverage': 0.3}
    )
    
    # Evaluate some text
    result = evaluator.evaluate("Your input text here")
    print(f"Combined score: {result.combined_score:.2f}")
    print(f"Passed: {result.passed(threshold=0.8)}")
"""

from .evaluation_result import EvaluationResult
from .task_evaluator import TaskEvaluator

__all__ = ['EvaluationResult', 'TaskEvaluator']
