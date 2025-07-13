#!/usr/bin/env python3
"""
Analysis utilities for refinement results CSV.
Demonstrates different query capabilities and provides plotting functions.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Any
import argparse

class RefinementAnalyzer:
    """Analyzes refinement results from CSV data."""
    
    def __init__(self, csv_path: Path):
        """Initialize with CSV file path."""
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load the CSV data."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        self.df = pd.read_csv(self.csv_path)
        print(f"Loaded {len(self.df)} rows from {self.csv_path}")
        print(f"Columns: {list(self.df.columns)}")
    
    def get_example_refinement_process(self, example_id: str) -> pd.DataFrame:
        """Get the entire refinement process for a specific example."""
        return self.df[self.df['example_id'] == example_id].sort_values('iteration_number')
    
    def get_average_scores_by_iteration(self) -> pd.DataFrame:
        """Get average scores across all examples for each iteration."""
        return self.df.groupby('iteration_number').agg({
            'combined_score': 'mean',
            'structure_score': 'mean',
            'coverage_score': 'mean',
            'focus_relevance_score': 'mean',
            'redundancy_score': 'mean'
        }).reset_index()
    
    def get_final_scores_summary(self) -> pd.DataFrame:
        """Get summary of final scores for all examples."""
        final_iterations = self.df[self.df['is_final_iteration'] == True]
        return final_iterations[['example_id', 'title', 'current_best_score', 'total_iterations']].sort_values('current_best_score', ascending=False)
    
    def get_convergence_stats(self) -> Dict[str, Any]:
        """Get convergence statistics."""
        final_iterations = self.df[self.df['is_final_iteration'] == True]
        
        total_examples = len(final_iterations)
        converged_early = len(final_iterations[final_iterations['converged_early'] == True])
        
        return {
            'total_examples': total_examples,
            'converged_early': converged_early,
            'convergence_rate': converged_early / total_examples if total_examples > 0 else 0,
            'avg_iterations': final_iterations['total_iterations'].mean(),
            'avg_final_score': final_iterations['current_best_score'].mean()
        }
    
    def get_judge_performance_comparison(self) -> pd.DataFrame:
        """Compare performance of different judges."""
        judge_scores = self.df[['structure_score', 'coverage_score', 'focus_relevance_score', 'redundancy_score']].mean()
        return judge_scores.to_frame('average_score').reset_index().rename(columns={'index': 'judge'})
    
    def plot_score_trends(self, save_path: Path = None):
        """Plot score trends across iterations."""
        avg_scores = self.get_average_scores_by_iteration()
        
        plt.figure(figsize=(12, 8))
        
        # Plot all judge scores
        plt.subplot(2, 2, 1)
        for score_col in ['structure_score', 'coverage_score', 'focus_relevance_score', 'redundancy_score']:
            plt.plot(avg_scores['iteration_number'], avg_scores[score_col], marker='o', label=score_col.replace('_score', ''))
        plt.xlabel('Iteration')
        plt.ylabel('Average Score')
        plt.title('Judge Scores by Iteration')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot combined score
        plt.subplot(2, 2, 2)
        plt.plot(avg_scores['iteration_number'], avg_scores['combined_score'], marker='o', color='red', linewidth=2)
        plt.xlabel('Iteration')
        plt.ylabel('Average Combined Score')
        plt.title('Combined Score Trend')
        plt.grid(True, alpha=0.3)
        
        # Plot final score distribution
        plt.subplot(2, 2, 3)
        final_scores = self.df[self.df['is_final_iteration'] == True]['current_best_score']
        plt.hist(final_scores, bins=20, alpha=0.7, color='green')
        plt.xlabel('Final Combined Score')
        plt.ylabel('Number of Examples')
        plt.title('Distribution of Final Scores')
        plt.grid(True, alpha=0.3)
        
        # Plot iterations distribution
        plt.subplot(2, 2, 4)
        iterations = self.df[self.df['is_final_iteration'] == True]['total_iterations']
        plt.hist(iterations, bins=range(1, max(iterations) + 2), alpha=0.7, color='orange')
        plt.xlabel('Total Iterations')
        plt.ylabel('Number of Examples')
        plt.title('Distribution of Iterations Needed')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        else:
            plt.show()
    
    def print_summary_report(self):
        """Print a comprehensive summary report."""
        print("\n" + "="*80)
        print("REFINEMENT ANALYSIS SUMMARY REPORT")
        print("="*80)
        
        # Basic stats
        convergence_stats = self.get_convergence_stats()
        print(f"\n📊 CONVERGENCE STATISTICS:")
        print(f"  Total examples processed: {convergence_stats['total_examples']}")
        print(f"  Examples converged early: {convergence_stats['converged_early']}")
        print(f"  Convergence rate: {convergence_stats['convergence_rate']:.2%}")
        print(f"  Average iterations needed: {convergence_stats['avg_iterations']:.2f}")
        print(f"  Average final score: {convergence_stats['avg_final_score']:.3f}")
        
        # Judge performance
        judge_performance = self.get_judge_performance_comparison()
        print(f"\n👨‍⚖️  JUDGE PERFORMANCE (Average Scores):")
        for _, row in judge_performance.iterrows():
            print(f"  {row['judge'].replace('_score', '').title()}: {row['average_score']:.3f}")
        
        # Top and bottom performers
        final_scores = self.get_final_scores_summary()
        print(f"\n🏆 TOP 3 PERFORMERS:")
        for _, row in final_scores.head(3).iterrows():
            print(f"  {row['title'][:50]}... (Score: {row['current_best_score']:.3f}, Iterations: {row['total_iterations']})")
        
        print(f"\n📉 BOTTOM 3 PERFORMERS:")
        for _, row in final_scores.tail(3).iterrows():
            print(f"  {row['title'][:50]}... (Score: {row['current_best_score']:.3f}, Iterations: {row['total_iterations']})")
        
        print("\n" + "="*80)

def main():
    """Main function to run analysis."""
    parser = argparse.ArgumentParser(description='Analyze refinement results from CSV')
    parser.add_argument('csv_file', type=str, help='Path to the refinement results CSV file')
    parser.add_argument('--plot', action='store_true', help='Generate and save plots')
    parser.add_argument('--example-id', type=str, help='Show detailed process for specific example ID')
    
    args = parser.parse_args()
    
    csv_path = Path(args.csv_file)
    
    try:
        analyzer = RefinementAnalyzer(csv_path)
        
        # Print summary report
        analyzer.print_summary_report()
        
        # Show specific example if requested
        if args.example_id:
            print(f"\n📋 DETAILED PROCESS FOR EXAMPLE {args.example_id}:")
            example_data = analyzer.get_example_refinement_process(args.example_id)
            if not example_data.empty:
                for _, row in example_data.iterrows():
                    print(f"\nIteration {row['iteration_number']}:")
                    print(f"  Combined Score: {row['combined_score']:.3f}")
                    print(f"  Structure: {row['structure_score']:.3f}")
                    print(f"  Coverage: {row['coverage_score']:.3f}")
                    print(f"  Focus/Relevance: {row['focus_relevance_score']:.3f}")
                    print(f"  Redundancy: {row['redundancy_score']:.3f}")
                    print(f"  Converged Early: {row['converged_early']}")
            else:
                print(f"Example ID '{args.example_id}' not found.")
        
        # Generate plots if requested
        if args.plot:
            plot_path = csv_path.with_suffix('.png')
            analyzer.plot_score_trends(plot_path)
    
    except Exception as e:
        print(f"Error analyzing data: {e}")

if __name__ == "__main__":
    main() 