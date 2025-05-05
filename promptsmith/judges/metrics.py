from typing import Any, Optional, Literal, Union
import dspy
from dspy.evaluate import Evaluate
from dspy.teleprompt import MIPROv2
from judges.judge_meaning import JudgeMeaning

"""
This file contains metrics and evaluation functions for all judges.

score_agreement_metric: Checks if predicted score matches gold score within tolerance
evaluate_judge: Tests judge accuracy on test data
calibrate_judge: Improves judge prompts using MIPROv2 optimization

Used to evaluate and improve all types of judges.
"""


def score_agreement_metric(
    example: dspy.Example,
    pred: dspy.Prediction,
    score_field: str = "score",
    gold_field: str = "gold_score"
) -> float:
    """General agreement metric for any judge with numeric scores."""
    pred_score = float(getattr(pred, score_field))
    gold_score = float(getattr(example, gold_field))
    diff = abs(pred_score - gold_score)
    return max(0.0, 1 - diff)


def evaluate_judge(judge_module, testset, metric=score_agreement_metric):
    """Return accuracy on a held‑out test set."""
    return Evaluate(devset=testset, metric=metric)(judge_module)


def calibrate_judge(
    devset,
    judge_class=JudgeMeaning,
    metric=score_agreement_metric,
    auto: Union[Literal['light', 'medium', 'heavy'], None] = None,
    num_candidates: int = 3,
    max_labeled_demos: int = 2,
    max_bootstrapped_demos: int = 1,
    seed: int = 42,
    num_trials: int = 5
) -> tuple[dspy.Predict, bool]:
    """
    Optimise the judge prompt with MIPROv2.
    Prints baseline and tuned dev accuracy, returns the tuned module.
    """
    baseline_model = dspy.Predict(judge_class)
    baseline_acc = Evaluate(devset=devset, metric=metric)(baseline_model)
    if isinstance(baseline_acc, tuple):
        baseline_acc = baseline_acc[0]
    print(f"Baseline dev acc: {baseline_acc:.3f}")

    teleprompter = MIPROv2(
        metric = metric,
        task_model = judge_class,
        auto = auto,      
        num_candidates = num_candidates,          
        max_labeled_demos = max_labeled_demos,          
        max_bootstrapped_demos = max_bootstrapped_demos,       
        seed = seed
    )

    tuned_model = teleprompter.compile(
        student = baseline_model,
        trainset = devset,
        num_trials = num_trials,
        minibatch = True,      
        requires_permission_to_run = False 
    )
    tuned_acc = Evaluate(devset=devset, metric=metric)(tuned_model)
    if isinstance(tuned_acc, tuple):
        tuned_acc = tuned_acc[0]
    print(f"Tuned dev acc: {tuned_acc:.3f}")

    found_optimized = tuned_acc > baseline_acc

    return tuned_model, found_optimized