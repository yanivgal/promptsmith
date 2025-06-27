from dataclasses import dataclass, field
from typing import Dict

@dataclass
class EvaluationResult:
    """
    Represents the result of evaluating a task output against multiple judges.
    
    This class holds the output text, individual judge scores and reasonings,
    weights for each judge, and the combined weighted score.
    
    Attributes:
        output: The text that was evaluated
        scores: Dictionary mapping judge names to their numeric scores
        reasonings: Dictionary mapping judge names to their textual feedback
        weights: Weights for each judge (default: equal weights)
        combined_score: The weighted average score (always calculated)
    """
    output: str
    scores: Dict[str, float]
    reasonings: Dict[str, str]
    weights: Dict[str, float] = field(default_factory=dict)
    combined_score: float = field(init=False)
    
    def __post_init__(self):
        # Set default equal weights if none provided
        if not self.weights and self.scores:
            self.weights = {name: 1.0/len(self.scores) for name in self.scores}
        
        # Always calculate combined score on initialization
        self._calculate_combined_score()
    
    def _calculate_combined_score(self) -> None:
        """Calculate and set the weighted average score."""
        if not self.weights or not self.scores:
            self.combined_score = 0.0
            return
            
        total_weight = sum(self.weights.values())
        if total_weight <= 0:
            self.combined_score = 0.0
            return
            
        weighted_sum = sum(
            self.scores[judge] * self.weights[judge]
            for judge in self.scores
            if judge in self.weights
        )
        self.combined_score = weighted_sum / total_weight
    
    def passed(self, threshold: float = 0.8) -> bool:
        """Check if the combined score meets or exceeds the threshold.
        
        Args:
            threshold: Minimum score to pass (default: 0.8)
            
        Returns:
            True if combined score meets or exceeds threshold, False otherwise
        """
        return self.combined_score >= threshold
