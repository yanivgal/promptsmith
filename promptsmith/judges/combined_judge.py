import dspy

class CombinedJudge(dspy.Module):
    def __init__(self, judge1, judge2):
        super().__init__()

        self.judge1 = dspy.Predict(judge1)
        self.judge2 = dspy.Predict(judge2)

    def forward(self, input_text, output_text):

        j1 = self.judge1(input_text=input_text, output_text=output_text)
        j2 = self.judge2(input_text=input_text, output_text=output_text)

        total_score = (j1.score + j2.score) / 2

        return dspy.Prediction(
            score=total_score,
            judge1_score=j1.score,
            judge1_reasoning=j1.reasoning,
            judge2_score=j2.score,
            judge2_reasoning=j2.reasoning
        )