from typing import Dict, Optional, Any
import dspy
from .evaluation_result import EvaluationResult

class TaskEvaluator:
    """
    Coordinates running a task and evaluating its output using multiple judges.
    
    This class handles the complete evaluation pipeline:
    1. Running the task on input text (if output not provided)
    2. Evaluating the output against all specified judges
    3. Calculating combined scores when weights are provided
    
    Example:
        evaluator = TaskEvaluator(
            task=dspy.ChainOfThought(BulletizeText),
            judges={
                'structure': dspy.Predict(JudgeBulletStructure),
                'coverage': dspy.Predict(JudgeCoverage)
            },
            weights={'structure': 0.7, 'coverage': 0.3}
        )
        result = evaluator.evaluate("Your input text here")
    """
    
    def __init__(
        self, 
        task: dspy.Module,
        judges: Dict[str, dspy.Module],
        weights: Optional[Dict[str, float]] = None
    ):
        """Initialize the TaskEvaluator.
        
        Args:
            task: The DSPy module that performs the main task
            judges: Dictionary mapping judge names to DSPy judge modules
            weights: Optional weights for each judge (default: equal weights).
                   Note: Weights should already be normalized (sum to 1.0).
        """
        self.task = task
        self.judges = judges
        self.weights = weights or {name: 1.0/len(judges) for name in judges}
    
    def evaluate(
        self, 
        input_text: str
    ) -> EvaluationResult:
        """Run the task and evaluate its output with all judges.
        
        Args:
            input_text: The input text to process
            
        Returns:
            EvaluationResult containing all scores, reasonings, and combined score
        """
        # Generate output using the task
        task_result = self.task(input_text=input_text)
        output = getattr(task_result, 'output_text', str(task_result))
        
        # Evaluate with all judges
        scores, reasonings = self._evaluate_with_judges(input_text, output)
        
        return EvaluationResult(
            output=output,
            scores=scores,
            reasonings=reasonings,
            weights=self.weights
        )
    
    def _get_judge_inputs(self, input_text: str, output: str, judge: dspy.Module) -> dict:
        """Prepare the correct input fields for a judge.
        
        All judges now consistently use 'input_text' and 'output_text' fields.
        """
        return {
            'input_text': input_text,
            'output_text': output
        }
    
    def _evaluate_with_judges(
        self, 
        input_text: str, 
        output: str
    ) -> tuple[Dict[str, float], Dict[str, str]]:
        """Run all judges on the given input and output.
        
        Handles different judge input field requirements dynamically.
        """
        scores = {}
        reasonings = {}
        
        for name, judge in self.judges.items():
            try:
                # Get the correct input fields for this judge
                judge_inputs = self._get_judge_inputs(input_text, output, judge)
                
                # Run the judge with the prepared inputs
                result = judge(**judge_inputs)
                scores[name] = result.score
                reasonings[name] = result.reasoning
            except Exception as e:
                scores[name] = 0.0
                reasonings[name] = f"Error during evaluation: {str(e)}"
        
        return scores, reasonings
