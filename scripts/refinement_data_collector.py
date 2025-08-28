#!/usr/bin/env python3
"""
Data collection structures and logic for refinement process.
Handles collecting and organizing refinement iteration data.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path
import csv
import json

@dataclass
class RefinementIteration:
    """Represents a single iteration in the refinement process."""

    iteration_number: int
    structure_score: float
    coverage_score: float
    focus_relevance_score: float
    redundancy_score: float
    combined_score: float
    structure_reasoning: str
    coverage_reasoning: str
    focus_relevance_reasoning: str
    redundancy_reasoning: str
    combined_feedback: str  # NEW: The aggregated feedback from all judges
    output: str
    refinement_reasoning: str
    is_final_iteration: bool
    converged_early: bool
    
    # Timing fields
    evaluation_time: float  # Time for all judges to evaluate
    aggregation_time: float  # Time for feedback aggregation
    refinement_time: float  # Time for refinement generation
    total_iteration_time: float  # Total time for this iteration

@dataclass
class RefinementResult:
    """Represents the complete refinement process for a single example."""
    example_id: str
    original_id: str
    title: str
    profession: str
    purpose: str
    original_text_length: int
    iterations: List[RefinementIteration]
    total_iterations: int
    max_combined_score: float
    iteration_of_max_combined_score: int
    
    # Timing fields
    total_refinement_time: float  # Total time for entire refinement process
    avg_time_per_iteration: float  # Average time per iteration

class RefinementDataCollector:
    """Collects and manages refinement data for multiple examples."""
    
    def __init__(self):
        self.results: List[RefinementResult] = []
        self.example_best_scores: Dict[str, float] = {}  # Track best score per example
    
    def add_result(self, result: RefinementResult):
        """Add a refinement result to the collection."""
        self.results.append(result)
    
    def get_all_iterations_for_csv(self) -> List[Dict[str, Any]]:
        """Convert all results to a flat list suitable for CSV export in long format."""
        csv_rows = []
        
        for result in self.results:
            current_best = 0.0
            current_best_iteration = 0
            
            for iteration in result.iterations:
                # Update current best for this example
                if iteration.combined_score > current_best:
                    current_best = iteration.combined_score
                    current_best_iteration = iteration.iteration_number
                
                row = {
                    'example_id': result.example_id,
                    'original_id': result.original_id,
                    'title': result.title,
                    'profession': result.profession,
                    'purpose': result.purpose,
                    'original_text_length': result.original_text_length,
                    'iteration_number': iteration.iteration_number,
                    'structure_score': round(iteration.structure_score, 4),
                    'coverage_score': round(iteration.coverage_score, 4),
                    'focus_relevance_score': round(iteration.focus_relevance_score, 4),
                    'redundancy_score': round(iteration.redundancy_score, 4),
                    'combined_score': round(iteration.combined_score, 4),
                    'structure_reasoning': iteration.structure_reasoning,
                    'coverage_reasoning': iteration.coverage_reasoning,
                    'focus_relevance_reasoning': iteration.focus_relevance_reasoning,
                    'redundancy_reasoning': iteration.redundancy_reasoning,
                    'combined_feedback': iteration.combined_feedback, 
                    'output': iteration.output,
                    'refinement_reasoning': iteration.refinement_reasoning,
                    'is_final_iteration': iteration.is_final_iteration,
                    'converged_early': iteration.converged_early,
                    'total_iterations': result.total_iterations,
                    'current_best_score': round(current_best, 4),
                    'current_best_iteration': current_best_iteration,
                    # Timing fields
                    'evaluation_time': round(iteration.evaluation_time, 3),
                    'aggregation_time': round(iteration.aggregation_time, 3),
                    'refinement_time': round(iteration.refinement_time, 3),
                    'total_iteration_time': round(iteration.total_iteration_time, 3),
                    'total_refinement_time': round(result.total_refinement_time, 3),
                    'avg_time_per_iteration': round(result.avg_time_per_iteration, 3)
                }
                csv_rows.append(row)
        
        return csv_rows
    
    def save_to_csv(self, output_path: Path):
        """Save all results to CSV in long format."""
        csv_rows = self.get_all_iterations_for_csv()
        
        if not csv_rows:
            print("No data to save")
            return
        
        fieldnames = csv_rows[0].keys()
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)
        
        print(f"Saved {len(csv_rows)} rows to {output_path}")
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for all refinement results."""
        if not self.results:
            return {}
        
        total_examples = len(self.results)
        total_iterations = sum(r.total_iterations for r in self.results)
        avg_iterations = total_iterations / total_examples
        avg_final_score = sum(r.max_combined_score for r in self.results) / total_examples
        
        converged_early_count = sum(
            1 for r in self.results 
            for i in r.iterations 
            if i.converged_early
        )
        
        # Timing statistics
        total_time = sum(r.total_refinement_time for r in self.results)
        avg_time_per_example = total_time / total_examples
        avg_time_per_iteration = sum(r.avg_time_per_iteration for r in self.results) / total_examples
        
        # Phase timing breakdown
        total_evaluation_time = sum(
            sum(i.evaluation_time for i in r.iterations) for r in self.results
        )
        total_aggregation_time = sum(
            sum(i.aggregation_time for i in r.iterations) for r in self.results
        )
        total_refinement_time_phase = sum(
            sum(i.refinement_time for i in r.iterations) for r in self.results
        )
        
        return {
            'total_examples': total_examples,
            'total_iterations': total_iterations,
            'average_iterations_per_example': avg_iterations,
            'average_final_score': avg_final_score,
            'examples_converged_early': converged_early_count,
            'convergence_rate': converged_early_count / total_examples if total_examples > 0 else 0,
            # Timing statistics
            'total_time': total_time,
            'average_time_per_example': avg_time_per_example,
            'average_time_per_iteration': avg_time_per_iteration,
            'total_evaluation_time': total_evaluation_time,
            'total_aggregation_time': total_aggregation_time,
            'total_refinement_time_phase': total_refinement_time_phase,
            'evaluation_time_percentage': (total_evaluation_time / total_time * 100) if total_time > 0 else 0,
            'aggregation_time_percentage': (total_aggregation_time / total_time * 100) if total_time > 0 else 0,
            'refinement_time_percentage': (total_refinement_time_phase / total_time * 100) if total_time > 0 else 0
        } 