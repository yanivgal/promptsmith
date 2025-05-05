from .judge_meaning         import JudgeMeaning
from .judge_readability     import JudgeReadability
from .judge_structure       import JudgeStructure
from .judge_conciseness     import JudgeConciseness
from .judge_focus_relevance import JudgeFocusRelevance

REGISTRY = {
    "meaning":         JudgeMeaning,
    "readability":     JudgeReadability,
    "structure":       JudgeStructure,
    "conciseness":     JudgeConciseness,
    "focus_relevance": JudgeFocusRelevance,
}