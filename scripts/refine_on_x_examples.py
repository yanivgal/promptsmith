#!/usr/bin/env python3
"""
Script to run refinement on X examples from the documents_train.csv file.
Supports command line arguments to specify the number of examples to process.
"""

import argparse
from pathlib import Path

from csv_loader import load_and_select_document_examples, get_default_csv_path

from promptsmith.dspy_init import get_dspy
from promptsmith.tasks.bad_to_good.bulletize_text_2 import BulletizeText
from promptsmith.judges.judge_bullet_structure import JudgeBulletStructure
from promptsmith.judges.judge_coverage import JudgeCoverage
from promptsmith.judges.judge_focus_relevance import JudgeFocusRelevance
from promptsmith.judges.judge_redundancy import JudgeRedundancy
from promptsmith.refiners import Refiner
from promptsmith.refiners.feedback_aggregator import FeedbackAggregator
from promptsmith.evaluation.task_evaluator import TaskEvaluator
from promptsmith.utils.display import display_evaluation_result

from scripts.enhanced_orchestrator import EnhancedRefinementOrchestrator
from scripts.refinement_data_collector import RefinementDataCollector


def setup_refinement_orchestrator(max_iterations=5, score_threshold=0.90):

    dspy, lm = get_dspy()
    
    bulletize_text_evaluator = TaskEvaluator(
        task=dspy.ChainOfThought(BulletizeText),
        judges={
            'structure': dspy.Predict(JudgeBulletStructure),
            'coverage': dspy.Predict(JudgeCoverage),
            'focus_relevance': dspy.Predict(JudgeFocusRelevance),
            'redundancy': dspy.Predict(JudgeRedundancy)
        },
        weights={
            'structure': 0.5,
            'coverage': 0.2,
            'focus_relevance': 0.15,
            'redundancy': 0.15,
        }
    )
    
    feedback_aggregator = dspy.Predict(FeedbackAggregator)
    
    orchestrator = EnhancedRefinementOrchestrator(
        evaluator=bulletize_text_evaluator,
        refiner=dspy.ChainOfThought(Refiner),
        feedback_aggregator=feedback_aggregator,
        max_iterations=max_iterations,
        score_threshold=score_threshold
    )
    
    return orchestrator

def run_refinement_on_examples(examples, orchestrator, data_collector):
    """
    Run refinement on the selected examples with detailed data collection.
    
    Args:
        examples: List of example dictionaries
        orchestrator: EnhancedRefinementOrchestrator instance
        data_collector: RefinementDataCollector instance
    
    Returns:
        List of refinement results
    """
    results = []

    for i, example in enumerate(examples, 1):
        print(f"\n{'='*80}")
        print(f"Processing example {i}/{len(examples)}")
        print(f"Title: {example['title']}")
        print(f"Profession: {example['profession']}")
        print(f"Purpose: {example['purpose']}")
        print(f"Text length: {len(example['text'])} characters")
        print(f"Original ID: {example['original_id']}")
        print(f"{'='*80}")
        
        # Run refinement with data collection
        try:
            # prepare example info for the enhanced orchestrator
            example_info = {
                'id': f"example_{i:03d}",
                'original_id': example['original_id'],
                'title': example['title'],
                'profession': example['profession'],
                'purpose': example['purpose']
            }
            
            refinement_result = orchestrator.refine_with_data_collection(
                example['text'], 
                example_info
            )

            # add to data collector
            data_collector.add_result(refinement_result)
            
            results.append({
                'example': example,
                'refinement_result': refinement_result
            })
            
            # print the best output
            best_iteration = refinement_result.iterations[refinement_result.iteration_of_max_combined_score - 1]
            print(f"Best refined output:")
            print(f"Best score: {refinement_result.max_combined_score:.3f}")
            print(f"Best iteration: {refinement_result.iteration_of_max_combined_score}")
            print(f"Total iterations: {refinement_result.total_iterations}")
            
        except Exception as e:
            print(f"Error processing example {i}: {e}")
            results.append({
                'example': example,
                'refinement_result': None,
                'error': str(e)
            })
    
    return results

def main():
    """Main function to run the refinement process."""
    
    parser = argparse.ArgumentParser(description='Run refinement on examples from documents_train.csv')
    parser.add_argument('-n', '--num_examples', type=int, default=1, 
                       help='Number of examples to process (default: 1)')
    parser.add_argument('-o', '--output', type=str, default='refinement_results',
                       help='Output file name (default: refinement_results)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for reproducibility (default: 42)')
    parser.add_argument('--max-iterations', type=int, default=5,
                       help='Maximum number of refinement iterations (default: 5)')
    parser.add_argument('-t','--threshold', type=float, default=0.90,
                       help='Score threshold for convergence (default: 0.90)')
    
    args = parser.parse_args()
    
    # configuration
    csv_path = get_default_csv_path()
    num_examples = args.num_examples
    max_iterations = args.max_iterations
    score_threshold = args.threshold
    output_file = Path(args.output)
    
    print(f"\nStarting refinement process on {num_examples} example(s) from documents_train.csv")
    print("=" * 80 + "\n")
    
    # load and select examples
    examples = load_and_select_document_examples(csv_path, num_examples, args.seed)

    # set up the refinement orchestrator and data collector
    print("\nSetting up refinement orchestrator...")
    orchestrator = setup_refinement_orchestrator(max_iterations, score_threshold)
    data_collector = RefinementDataCollector()
    
    # run refinement on the examples
    print("\nRunning refinement on selected examples:")
    results = run_refinement_on_examples(examples, orchestrator, data_collector)
    
    # save detailed results to CSV
    csv_output_file = output_file.with_suffix('.csv')
    print(f"\nSaving detailed results to {csv_output_file}...")
    data_collector.save_to_csv(csv_output_file)
    
    # print summary
    print("\n" + "=" * 80)
    print("REFINEMENT PROCESS COMPLETE")
    print("=" * 80)
    
    successful_results = [r for r in results if r['refinement_result'] is not None]
    print(f"Successfully processed: {len(successful_results)}/{len(results)} examples")
    
    if successful_results:
        avg_score = sum(r['refinement_result'].max_combined_score for r in successful_results) / len(successful_results)
        print(f"Average best score: {avg_score:.3f}")
        
        avg_iterations = sum(r['refinement_result'].total_iterations for r in successful_results) / len(successful_results)
        print(f"Average iterations: {avg_iterations:.1f}")
    
    # print detailed statistics
    summary_stats = data_collector.get_summary_stats()
    if summary_stats:
        print(f"\nDetailed Statistics:")
        print(f"  Total examples: {summary_stats['total_examples']}")
        print(f"  Total iterations: {summary_stats['total_iterations']}")
        print(f"  Average iterations per example: {summary_stats['average_iterations_per_example']:.2f}")
        print(f"  Average final score: {summary_stats['average_final_score']:.3f}")
        print(f"  Examples converged early: {summary_stats['examples_converged_early']}")
        print(f"  Convergence rate: {summary_stats['convergence_rate']:.2%}")
    
    print(f"\nDetailed results saved to: {csv_output_file}")



if __name__ == "__main__":
    main() 