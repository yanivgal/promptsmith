import streamlit as st
import importlib
import pkgutil
import os
from promptsmith.dspy_init import get_dspy

# Must be the first Streamlit command
st.set_page_config(page_title="PromptSmith Workbench", layout="centered")

# Initialize DSPy only once at the start
if 'dspy' not in st.session_state:
    dspy, lm = get_dspy()
    st.session_state['dspy'] = dspy
    st.session_state['lm'] = lm
else:
    dspy = st.session_state['dspy']
    lm = st.session_state['lm']

st.title("PromptSmith Workbench")

# --- Helper functions to dynamically load tasks and judges ---
def get_module_names(package):
    return [name for _, name, ispkg in pkgutil.iter_modules(package.__path__) if not ispkg and not name.startswith("__")]

def get_class_names(module):
    return [name for name in dir(module) if not name.startswith("__") and isinstance(getattr(module, name), type)]

# --- Load tasks and judges ---
import promptsmith.tasks as tasks_pkg
import promptsmith.judges as judges_pkg

task_modules = get_module_names(tasks_pkg)
judge_modules = get_module_names(judges_pkg)

task_options = [name for name in task_modules if name != "__init__"]
judge_options = [name for name in judge_modules if name != "__init__"]

# --- UI Layout ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("**before**")
    before_text = st.text_area("Input text (before)", height=300, key="before_text", label_visibility="collapsed")

st.markdown("---")

col3, col4, col5 = st.columns([2,2,1])

with col3:
    selected_task = st.selectbox("select task:", task_options, key="task_select")
with col4:
    selected_judge = st.selectbox("select judge:", judge_options, key="judge_select")
with col5:
    transform_clicked = st.button("transform")

# --- Process text and evaluate results ---
if 'after_text' not in st.session_state:
    st.session_state['after_text'] = ""
if 'diff_summary' not in st.session_state:
    st.session_state['diff_summary'] = ""
if 'eval_results' not in st.session_state:
    st.session_state['eval_results'] = ""

if transform_clicked and before_text:
    try:
        # Dynamically import and run the selected task
        task_module = importlib.import_module(f"promptsmith.tasks.{selected_task}")
        task_class = getattr(task_module, selected_task.split('_')[0].title() + selected_task.split('_')[1].title())
        task = dspy.ChainOfThought(task_class)
        transformed_result = task(input_text=before_text)
        st.session_state["after_text"] = transformed_result.output_text

        # Get the differences
        from promptsmith.tasks.restructure_delta import RestructureDelta
        delta = dspy.ChainOfThought(RestructureDelta)
        diff_result = delta(input_text=before_text, output_text=transformed_result.output_text)
        st.session_state["diff_summary"] = diff_result.summary_of_differences

        # Run the evaluation
        judge_path = os.path.abspath(f"promptsmith/judges/judge_{selected_task}.yaml")
        from promptsmith.judges.ensemble_judge import EnsembleJudge
        judge = EnsembleJudge(judge_path)
        verdict = judge(input_text=before_text, output_text=transformed_result.output_text)
        
        # Format evaluation results
        eval_summary = f"Overall Score: {verdict.combined_score:.3f}\n\n"
        
        # Get all judge names from the verdict attributes
        judge_names = [attr.split('_')[0] for attr in dir(verdict) if attr.endswith('_score')]
        
        for name in judge_names:
            score = getattr(verdict, f"{name}_score")
            weight = getattr(verdict, f"{name}_weight")
            reasoning = getattr(verdict, f"{name}_reasoning")
            eval_summary += f"{name.replace('_', ' ').title()} (score={score:.2f}, weight={weight}):\n"
            eval_summary += f"{reasoning}\n\n"
            
        st.session_state["eval_results"] = eval_summary

    except Exception as e:
        st.error(f"Error processing text: {str(e)}")
        st.session_state["after_text"] = f"Error: {str(e)}"
        st.session_state["diff_summary"] = "Error occurred during processing"
        st.session_state["eval_results"] = "Error occurred during evaluation"

# --- Show transformed text in the 'after' box ---
with col2:
    st.markdown("**after**")
    st.markdown(
        st.session_state["after_text"],
        unsafe_allow_html=True
    )

# --- Summary of differences ---
st.markdown("**summary of differences:**")
st.markdown(
    st.session_state["diff_summary"],
    unsafe_allow_html=True
)

# --- Evaluation results ---
st.markdown("**evaluation results:**")
st.markdown(
    st.session_state["eval_results"],
    unsafe_allow_html=True
) 