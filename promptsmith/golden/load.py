import yaml
import random
import dspy

def load_golden_set(judge_name: str,
                    dev_frac: float = 0.8,
                    seed: int = 42):
    """Read YAML, build DSPy Examples, split dev/test."""
    
    path = f"golden/{judge_name}.yaml"
    with open(path, "r", encoding="utf‑8") as f:
        raw = yaml.safe_load(f)

    exs = []
    for row in raw:
        ex = dspy.Example(
            input_text=row["input"],
            output_text=row["candidate"],
            gold_score=row["score"],
            gold_reasoning =row["reasoning"]
        ).with_inputs("input_text", "output_text")
        exs.append(ex)

    rng = random.Random(seed)
    rng.shuffle(exs)
    split = int(len(exs) * dev_frac)
    return exs[:split], exs[split:]