# PromptSmith

![PromptSmith logo](assets/promptsmith.png)

**PromptSmith** is a small workbench built with [DSPy](https://github.com/stanfordnlp/dspy) for experimenting with prompt engineering and custom evaluation judges. It provides a few text‑transformation tasks, scoring modules, and a self‑refinement loop to iteratively improve LLM outputs.

## Features

- **Tasks** – sample DSPy `Signature`s for rewriting text such as `BulletizeText` and `RestructureText`.
- **Judges** – evaluation modules (e.g. `JudgeMeaning`, `JudgeCoverage`, `JudgeBulletStructure`) that score an output against the original input.
- **Ensemble judging** – YAML configs combine multiple judges with weights to produce a single verdict.
- **Refinement loop** – the `RefinementOrchestrator` runs a task, evaluates it and asks a refiner module to fix the worst aspect until a target score is met.
- **Streamlit apps** – `app.py` exposes the tasks and judges in a simple web UI. `bullet_battle.py` lets a human compare two versions of bulletised text.
- **Jupyter notebooks** – examples showing how to use DSPy together with the provided modules.

## Setup

1. Clone this repository.
2. Install the dependencies (editable install recommended):
   ```bash
   pip install -e .
   ```
   or
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your `OPENAI_API_KEY`.

## Usage

### Running the web UI

Launch the main workbench using Streamlit:

```bash
streamlit run app.py
```

You can then paste text, choose a task and a judge, and see the transformed output along with structured feedback.

`bullet_battle.py` is a smaller app for manually choosing which of two bulletised versions is better:

```bash
streamlit run bullet_battle.py
```

### Using the modules in code

```python
from promptsmith.dspy_init import get_dspy
from promptsmith.tasks.bulletize_text import BulletizeText
from promptsmith.evaluation.task_evaluator import TaskEvaluator
from promptsmith.judges.ensemble_judge import EnsembleJudge

# initialise DSPy and the language model
dspy, _ = get_dspy()

# build the task and evaluation pipeline
task = dspy.ChainOfThought(BulletizeText)
judge = EnsembleJudge('promptsmith/judges/judge_bulletize_text.yaml')
evaluator = TaskEvaluator(task=task, judges={"outline": judge})

result = evaluator.evaluate("Long text to summarise ...")
print(result.scores, result.combined_score)
```

Consult the notebooks in `notebooks/` for more detailed examples and analysis.

## Self-Refine

PromptSmith includes an iterative "self-refinement" loop inspired by the
[Self-Refine](https://arxiv.org/abs/2303.17651) paper. After a task runs, its
output is scored by a set of judges. A `Refiner` module then attempts to fix the
worst issues and the cycle repeats until a target score is met.

Below is a simplified example from `notebooks/refine/refine copy 2.ipynb` showing
how to set up the refinement orchestrator:

```python
dspy, _ = get_dspy()
with open('data/text_01.txt') as f:
    text = f.read()

evaluator = TaskEvaluator(
    task=dspy.ChainOfThought(BulletizeText),
    judges={
        'structure': dspy.Predict(JudgeBulletStructure),
        'coverage': dspy.Predict(JudgeCoverage),
        'focus_relevance': dspy.Predict(JudgeFocusRelevance),
        'redundancy': dspy.Predict(JudgeRedundancy),
    },
    weights={
        'structure': 0.5,
        'coverage': 0.2,
        'focus_relevance': 0.15,
        'redundancy': 0.15,
    },
)

orchestrator = RefinementOrchestrator(
    evaluator=evaluator,
    refiner=dspy.Predict(Refiner),
    max_iterations=5,
    score_threshold=0.96,
)

orchestrator.refine(text)
```

The first and final iterations are stored in `orchestrator.history` for further
inspection.

## Contributing

Pull requests are welcome. Feel free to open an issue or submit a PR if you find problems or have ideas for improvements.

LLMs shine only when guided by clear instructions **and** reliable evaluation. PromptSmith helps you craft both so your models stay robust, even on tricky inputs.

