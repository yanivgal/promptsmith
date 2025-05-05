from pathlib import Path
import yaml

from ..judges import REGISTRY
import dspy

def get_input_fields(sig_cls):
    """
    Get the input fields for a judge.
    """
    return [
        name for name, field in sig_cls.model_fields.items()
        if field.json_schema_extra and field.json_schema_extra.get('__dspy_field_type') == 'input'
    ]

class EnsembleJudge(dspy.Module):
    def __init__(self, cfg_path):
        super().__init__()
        cfg = yaml.safe_load(Path(cfg_path).read_text())
        self.sub_judges = {}
        self.weights = {}
        self.input_fields = {}

        for name, opts in cfg.items():
            sig_cls = REGISTRY[name]
            compiled_path = opts.get("compiled")
            self.sub_judges[name] = (
                dspy.Predict.load(path=compiled_path) if compiled_path else dspy.Predict(sig_cls)
            )
            self.weights[name] = opts["weight"]
            self.input_fields[name] = get_input_fields(sig_cls)

    def _build_judge_kwargs(self, required_fields, **available_inputs):
        missing = [field for field in required_fields if field not in available_inputs]
        if missing:
            raise ValueError(f"Missing required fields for judge: {missing}")
        return {field: available_inputs[field] for field in required_fields}

    def forward(self, input_text, output_text):
        scores, reasons = {}, {}
        available_inputs = {"input_text": input_text, "output_text": output_text}
        for name, judge in self.sub_judges.items():
            required_fields = self.input_fields[name]
            judge_kwargs = self._build_judge_kwargs(required_fields, **available_inputs)
            result = judge(**judge_kwargs)
            scores[name] = result.score
            reasons[name] = result.reasoning

        total_w = sum(self.weights.values())
        combined = sum(self.weights[n] * scores[n] for n in scores) / total_w

        return dspy.Prediction(
            **{f"{n}_score": s for n, s in scores.items()},
            **{f"{n}_reasoning": r for n, r in reasons.items()},
            **{f"{n}_weight": self.weights[n] for n in self.weights},
            combined_score=combined
        )
