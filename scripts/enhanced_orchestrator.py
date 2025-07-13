#!/usr/bin/env python3
"""
Enhanced orchestrator that captures detailed iteration information for data collection.
Extends the base RefinementOrchestrator with data collection capabilities.
"""

from typing import Dict, Any, List, Optional
from promptsmith.refiners.orchestrator import RefinementOrchestrator
from promptsmith.evaluation.task_evaluator import TaskEvaluator
from promptsmith.evaluation.evaluation_result import EvaluationResult
from promptsmith.utils.display import display_evaluation_result
from promptsmith.refiners.feedback_aggregator import FeedbackAggregator
from .refinement_data_collector import RefinementIteration, RefinementResult

class EnhancedRefinementOrchestrator(RefinementOrchestrator):
    """Enhanced orchestrator that captures detailed iteration data for analysis."""
    
    def __init__(
        self,
        evaluator: TaskEvaluator,
        refiner,
        feedback_aggregator: FeedbackAggregator,
        max_iterations: int = 5,
        score_threshold: float = 0.9,
        verbose: bool = True
    ):
        """Initialize the enhanced orchestrator."""
        super().__init__(evaluator, refiner, feedback_aggregator, max_iterations, score_threshold, verbose)
        self.detailed_history: List[RefinementIteration] = []

    def refine_with_data_collection(
        self, 
        input_text: str, 
        example_info: Dict[str, Any]
    ) -> RefinementResult:
        """Run refinement with detailed data collection.
        
        Args:
            input_text: The initial input text to process
            example_info: Dictionary containing example metadata (id, title, profession, purpose)
            
        Returns:
            RefinementResult containing all iteration details
        """
        self.detailed_history = []
        self.history = []  # Reset history for this refinement run
        current_result = None
        current_output = None
        converged_early = False
        actual_iterations = 0

        if self.verbose:
            print("\n" + "="*80)
            print(f"🚀 Starting refinement process (max {self.max_iterations} iterations, target threshold: {self.score_threshold})")
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
                converged_early = True
                
                # Record the final iteration
                self._record_iteration(
                    iteration, current_result, None, "", converged_early, True
                )
                break

            # Check if this is the final iteration - if so, only evaluate, don't refine
            is_final = (iteration == self.max_iterations)
            if is_final:
                if self.verbose:
                    print(f"\n🏁 Final iteration reached - evaluating without refinement")
                
                # Record the final iteration (evaluation only)
                self._record_iteration(
                    iteration, current_result, None, "", False, True
                )
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
                task_type='bulletize',
                feedback_type='aggregated'
            )
            
            # Record this iteration before updating
            self._record_iteration(
                iteration, current_result, refinement.reasoning, combined_feedback, False, False
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

        # Create and return the complete refinement result
        # Find the iteration with the maximum combined score
        max_score_iteration = 1
        max_score = 0.0
        for i, iteration in enumerate(self.detailed_history, 1):
            if iteration.combined_score > max_score:
                max_score = iteration.combined_score
                max_score_iteration = i
        
        return RefinementResult(
            example_id=example_info.get('id', 'unknown'),
            original_id=example_info.get('original_id', 'unknown'),
            title=example_info.get('title', 'Untitled'),
            profession=example_info.get('profession', 'Unknown'),
            purpose=example_info.get('purpose', 'Unknown'),
            original_text_length=len(input_text),
            iterations=self.detailed_history,
            total_iterations=actual_iterations,
            max_combined_score=max_score,  # Use the actual max score, not the last score
            iteration_of_max_combined_score=max_score_iteration
        )

    def _record_iteration(
        self, 
        iteration_number: int, 
        result: EvaluationResult, 
        refinement_reasoning: Optional[str],
        combined_feedback: str,
        converged_early: bool,
        is_final_iteration: bool
    ):
        """Record detailed information for a single iteration."""
        iteration = RefinementIteration(
            iteration_number=iteration_number,
            structure_score=result.scores.get('structure', 0.0),
            coverage_score=result.scores.get('coverage', 0.0),
            focus_relevance_score=result.scores.get('focus_relevance', 0.0),
            redundancy_score=result.scores.get('redundancy', 0.0),
            combined_score=result.combined_score,
            structure_reasoning=result.reasonings.get('structure', ''),
            coverage_reasoning=result.reasonings.get('coverage', ''),
            focus_relevance_reasoning=result.reasonings.get('focus_relevance', ''),
            redundancy_reasoning=result.reasonings.get('redundancy', ''),
            combined_feedback=combined_feedback,  # NEW: Store the aggregated feedback
            output=result.output,
            refinement_reasoning=refinement_reasoning or '',
            is_final_iteration=is_final_iteration,
            converged_early=converged_early
        )
        self.detailed_history.append(iteration) 