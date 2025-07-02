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

## Contributing

Pull requests are welcome. Feel free to open an issue or submit a PR if you find problems or have ideas for improvements.

LLMs shine only when guided by clear instructions **and** reliable evaluation. PromptSmith helps you craft both so your models stay robust, even on tricky inputs.

