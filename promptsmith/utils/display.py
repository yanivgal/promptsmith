"""Utilities for displaying evaluation and refinement results in a minimal format."""
from typing import Dict, Any, Optional

def display_evaluation_result(
    result: Any,
    iteration: Optional[int] = None,
    refinement_type: Optional[str] = None,
) -> None:
    """Display an EvaluationResult in a minimal, focused format.
    
    Shows only the combined score, individual judge scores, and reasonings.
    """
    if not hasattr(result, 'scores'):
        print("Error: Invalid result object")
        return
    
    # Get attributes with defaults
    scores = getattr(result, 'scores', {})
    reasonings = getattr(result, 'reasonings', {})
    combined_score = getattr(result, 'combined_score', 0.0)
    
    print(f"\n{_color_score(combined_score, label="combined score")}")
    
    # Display each judge's score and reasoning
    for judge, score in scores.items():
        reasoning = reasonings.get(judge, "No reasoning provided").strip()
        colored_score = _color_score(score, label=judge)
        print(f"\n{colored_score}")
        print(f"{reasoning}")

    print("\n" + "-" * 60)

def _color_score(score: float, label: Optional[str] = None) -> str:
    """Color code a score and optionally add a label."""
    score_str = f"{score:.2f}"
    if label:
        score_str = f"{label}: {score_str}"
    
    if score >= 0.8:
        return f"\033[92m{score_str}\033[0m"  # Green
    elif score >= 0.5:
        return f"\033[93m{score_str}\033[0m"  # Yellow
    return f"\033[91m{score_str}\033[0m"  # Red
