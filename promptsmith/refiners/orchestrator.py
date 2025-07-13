"""Orchestrator for the self-refinement process.

This module contains the RefinementOrchestrator class that coordinates the
self-refinement loop using a task evaluator and a refiner.
"""

from typing import Dict, Any, List, Optional
from ..evaluation.task_evaluator import TaskEvaluator
from ..evaluation.evaluation_result import EvaluationResult
from ..utils.display import display_evaluation_result
from .feedback_aggregator import FeedbackAggregator

class RefinementOrchestrator:
    """Orchestrates the self-refinement process.
    
    This class manages the refinement loop, coordinating between the task,
    evaluator, and refiner to iteratively improve the output.
    """
    
    def __init__(
        self,
        evaluator: TaskEvaluator,
        refiner,
        feedback_aggregator: FeedbackAggregator,
        max_iterations: int = 5,
        score_threshold: float = 0.9,
        verbose: bool = True
    ):
        """Initialize the orchestrator.
        
        Args:
            evaluator: Configured TaskEvaluator instance
            refiner: The refiner to use for making improvements
            feedback_aggregator: The FeedbackAggregator to combine judge feedback
            max_iterations: Maximum number of refinement iterations
            score_threshold: Minimum score to consider the output satisfactory
            verbose: Whether to print progress information
        """
        self.evaluator = evaluator
        self.refiner = refiner
        self.feedback_aggregator = feedback_aggregator
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
        self.history = []
        current_result = None
        current_output = None
        actual_iterations = 0

        if self.verbose:
            print("\n" + "="*80)
            print(f"🚀 Starting refinement process (max {self.max_iterations} iterations)")
            print("="*80)

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

            # Aggregate feedback from all judges
            combined_feedback = self._aggregate_feedback(input_text, current_result)
            
            if self.verbose:
                print(f"\n📊 Aggregated feedback from {len(current_result.reasonings)} judges into a single combined feedback:\n")
                print(f"{combined_feedback}")
                print("\n🛠️  Generating refinement...")

            # Generate refined output using the DSPy module
            refinement = self.refiner(
                original_text=input_text,
                current_output=current_result.output,
                feedback=combined_feedback,
                task_type='bulletize',  # Default task type, can be made configurable
                feedback_type='aggregated'  # Using aggregated feedback from all judges
            )
            
            # Update current output for next iteration
            current_output = refinement.refined_output
            
            if self.verbose:
                print("✨ Refinement complete!\n")
                if hasattr(refinement, 'reasoning') and refinement.reasoning:
                    print(f"{refinement.reasoning}")
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

    def _aggregate_feedback(self, input_text: str, result: EvaluationResult) -> str:
        """Aggregate feedback from all judges using the FeedbackAggregator.
        
        Args:
            input_text: The original input text
            result: The evaluation result containing all judge feedback
            
        Returns:
            Combined feedback string from all judges
        """
        # Extract all feedback from judges
        all_feedback = list(result.reasonings.values())
        
        # Use the feedback aggregator to combine all feedback
        aggregated_result = self.feedback_aggregator(
            original_text=input_text,
            current_output=result.output,
            task_type='bulletize',  # Default task type, can be made configurable
            judges_feedback=all_feedback
        )
        
        return aggregated_result.combined_feedback

    def _get_worst_aspect(self, result: EvaluationResult) -> tuple[str, float]:
        """Return the name and score of the worst performing aspect."""
        return min(result.scores.items(), key=lambda x: x[1])