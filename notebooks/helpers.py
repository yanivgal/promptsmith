from IPython.display import display, HTML
from promptsmith.tasks.restructure_delta import RestructureDelta

def display_verdict(verdict):

    print("\n📊 Evaluation Results:")
    print("----------------------")
    
    store = verdict._store

    # Find all score, reasoning, and weight fields
    score_fields = [k for k in store if k.endswith('_score') and k != 'combined_score']
    reasoning_fields = [k for k in store if k.endswith('_reasoning')]
    weight_fields = {k.replace('_weight', ''): store[k] for k in store if k.endswith('_weight')}

    # Display overall score
    overall = store.get('combined_score')
    if overall is None and score_fields:
        # Fallback: average of all scores
        overall = sum(store[k] for k in score_fields) / len(score_fields)
    print(f"\n🌟 Overall Score: {overall:.3f}\n")

    # For each judge, display name, score, weight, and reasoning
    # Sort for consistent order
    for field in sorted(score_fields):
        judge_key = field.replace('_score', '')
        judge_name = judge_key.replace('_', ' ').title()
        reasoning_field = field.replace('_score', '_reasoning')
        score = store[field]
        reasoning = store.get(reasoning_field, "")
        weight = weight_fields.get(judge_key, None)
        if weight is not None:
            print(f"### {judge_name} Analysis (score={score:.2f}, weight={weight})")
        else:
            print(f"### {judge_name} Analysis (score={score:.2f})")
        print(reasoning)
        print()

def display_side_by_side(text1, text2, width="48%", padding="1%"):
    html = """
    <div style='display: flex; width: 100%;'>
        <div style='width: {width}; padding: {padding}; overflow: auto; border: 1px solid #ddd;'>
            <div style='font-weight: bold; margin-bottom: 10px;'>Original Text</div>
            <pre style='white-space: pre-wrap; word-wrap: break-word; max-width: 100%; margin: 0;'>{text1}</pre>
        </div>
        <div style='width: {width}; padding: {padding}; overflow: auto; border: 1px solid #ddd;'>
            <div style='font-weight: bold; margin-bottom: 10px;'>Transformed Text</div>
            <pre style='white-space: pre-wrap; word-wrap: break-word; max-width: 100%; margin: 0;'>{text2}</pre>
        </div>
    </div>
    """.format(width=width, padding=padding, text1=text1, text2=text2)
    display(HTML(html))


def display_original_transformed(dspy, original_text, transformed_text, verdict):
    
    display_side_by_side(original_text, transformed_text)
    display_verdict(verdict)

    summarize_differences = dspy.ChainOfThought(RestructureDelta)
    result = summarize_differences(input_text=original_text, output_text=transformed_text)

    print("🔍 Summary of Differences:")
    print(result.summary_of_differences)