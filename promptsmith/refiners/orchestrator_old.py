"""Orchestrator for the self-refinement process.

This module contains the RefinementOrchestrator class that coordinates the
self-refinement loop using a task evaluator and a refiner.
"""

from typing import Dict, Any, List, Optional
from ..evaluation.task_evaluator import TaskEvaluator
from ..evaluation.evaluation_result import EvaluationResult
from ..utils.display import display_evaluation_result

class RefinementLowestScoreOrchestrator:
    """Orchestrates the self-refinement process.
    
    This class manages the refinement loop, coordinating between the task,
    evaluator, and refiner to iteratively improve the output.
    """
    
    def __init__(
        self,
        evaluator: TaskEvaluator,
        refiner,
        max_iterations: int = 5,
        score_threshold: float = 0.9,
        verbose: bool = True
    ):
        """Initialize the orchestrator.
        
        Args:
            evaluator: Configured TaskEvaluator instance
            refiner: The refiner to use for making improvements
            max_iterations: Maximum number of refinement iterations
            score_threshold: Minimum score to consider the output satisfactory
            verbose: Whether to print progress information
        """
        self.evaluator = evaluator
        self.refiner = refiner
        self.max_iterations = max_iterations
        self.score_threshold = score_threshold
        self.verbose = verbose
        self.history: List[EvaluationResult] = []

    def refine(self, input_text: str) -> Dict[str, Any]:
        """Run the refinement loop.
        
        Args:
            input_text: The initial input text to process
            
        Returns:
            Dictionary containing:
            - output: The final refined output
            - result: The final EvaluationResult
            - iterations: Number of iterations performed
            - history: List of all EvaluationResults from each iteration
        """
        self.history = []  # Reset history for this refinement run
        current_result = None
        current_output = None
        actual_iterations = 0

        if self.verbose:
            print("\n" + "="*60)
            print(f"🚀 Starting refinement process (max {self.max_iterations} iterations)")
            print("="*60)

        for iteration in range(1, self.max_iterations + 1):
            actual_iterations = iteration
            if self.verbose:
                print(f"\n🔄 Iteration {iteration}/{self.max_iterations}")
                print("-" * 40)

            # Evaluate the current output (or generate initial output)
            if self.verbose:
                print("🔍 Evaluating current output...")
                
            current_result = self.evaluator.evaluate(input_text)
            self.history.append(current_result)

            # Display progress if verbose
            if self.verbose:
                display_evaluation_result(
                    result=current_result,
                    iteration=iteration,
                )

            # Check if we've met the threshold
            if current_result.passed(self.score_threshold):
                if self.verbose:
                    print(f"\n✅ Target score of {self.score_threshold} reached!")
                break

            # Get feedback from the worst performing aspect
            worst_aspect, worst_score = self._get_worst_aspect(current_result)
            feedback = current_result.reasonings[worst_aspect]
            
            if self.verbose:
                print(f"\n📊 Identified area for improvement: {worst_aspect} (score: {worst_score:.2f})")
                print("\n🛠️  Generating refinement...")

            # Generate refined output using the DSPy module
            refinement = self.refiner(
                original_text=input_text,
                current_output=current_result.output,
                feedback=feedback,
                task_type='bulletize',  # Default task type, can be made configurable
                feedback_type=worst_aspect  # Using the worst aspect as feedback type
            )
            
            # Update current output for next iteration
            current_output = refinement.refined_output
            
            if self.verbose:
                print("✨ Refinement complete!")
                if hasattr(refinement, 'reasoning') and refinement.reasoning:
                    print(f"📝 Reasoning: {refinement.reasoning}")
                print("\n" + "=" * 60)
            
            # Use the refined output as input for next iteration
            input_text = current_output
        else:
            if self.verbose:
                print(f"\n⚠️  Reached maximum iterations ({self.max_iterations}) without reaching target score")

        if self.verbose:
            print("\n" + "="*60)
            print(f"🏁 Refinement complete after {actual_iterations} iteration{'s' if actual_iterations != 1 else ''}")
            final_score = self.history[-1].combined_score if self.history else 0
            print("="*60 + "\n")

        return {
            'output': current_result.output if current_result else None,
            'result': current_result,
            'iterations': actual_iterations,
            'history': self.history
        }

    def _get_worst_aspect(self, result: EvaluationResult) -> tuple[str, float]:
        """Return the name and score of the worst performing aspect."""
        return min(result.scores.items(), key=lambda x: x[1])