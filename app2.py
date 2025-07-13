import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
from st_diff_viewer import diff_viewer

refinements_file = "r_10_5.csv"

@st.cache_data
def load_data():
    refinements = pd.read_csv(refinements_file)
    originals = pd.read_csv("data/documents_train.csv")
    return refinements, originals


def select_iteration(iteration_idx):

    iteration = st.session_state.example_df.iloc[iteration_idx]

    st.session_state.iteration_idx = iteration_idx
    st.session_state.iteration_row = iteration
    st.session_state.iteration_text_length = len(iteration["output"])


def select_example(refinements_df, originals_df, example_id = None):

    if example_id is None:
        if "example_id" in st.session_state:
            example_id = st.session_state.example_id
        else:
            example_id = refinements_df["example_id"].iloc[0]
            st.session_state.example_id = "empty_example_id"
        
    if example_id != st.session_state.example_id:

        example_df = refinements_df[refinements_df["example_id"] == example_id].sort_values("iteration_number").reset_index(drop=True)
        
        st.session_state.example_id = example_id
        st.session_state.example_df = example_df
        st.session_state.total_iterations = len(example_df)
        select_iteration(0)

        original_text_row = originals_df[originals_df["id"] == example_df["original_id"].iloc[0]]
        st.session_state.original_text = original_text_row["resource"].iloc[0] if not original_text_row.empty else "Original text not found."


def navigate_examples(refinements_df, originals_df, direction):
    """Navigate to previous or next example"""
    examples_ids = refinements_df["example_id"].unique()
    
    if "example_index" not in st.session_state:
        st.session_state.example_index = 0
    
    if direction == "prev" and st.session_state.example_index > 0:
        st.session_state.example_index -= 1
    elif direction == "next" and st.session_state.example_index < len(examples_ids) - 1:
        st.session_state.example_index += 1
    
    new_example_id = examples_ids[st.session_state.example_index]
    select_example(refinements_df, originals_df, new_example_id)


def render_navigation():

    total_iterations = st.session_state.total_iterations
    current_iteration = st.session_state.iteration_idx

    col1, col2, _, _, _, _, _, _, _, _, _, _ = st.columns(12)
    with col1:
        prev_clicked = st.button("⬅️ Prev", key="prev_iteration_button")
    with col2:
        next_clicked = st.button("Next ➡️", key="next_iteration_button")

    if prev_clicked and current_iteration > 0:
        current_iteration = st.session_state.iteration_idx
        select_iteration(current_iteration - 1)
    elif next_clicked and current_iteration < total_iterations - 1:
        current_iteration = st.session_state.iteration_idx
        select_iteration(current_iteration + 1)

    st.markdown(f"##### **Iteration:** {st.session_state.iteration_idx + 1} of {total_iterations}")
    st.markdown("<div style='padding-top: 1rem;'></div>", unsafe_allow_html=True)


def create_interactive_score_plot(example_df):

    fig = go.Figure()
    
    score_configs = [
        ("structure_score", "Structure"),
        ("coverage_score", "Coverage"), 
        ("focus_relevance_score", "Focus"),
        ("redundancy_score", "Redundancy"),
        ("combined_score", "Combined")
    ]
    
    for score_col, display_name in score_configs:
        is_combined = score_col == "combined_score"
        
        fig.add_trace(go.Scatter(
            x=example_df["iteration_number"],
            y=example_df[score_col],
            mode='lines+markers',
            name=display_name,
            line=dict(width=3, dash='dash') if is_combined else dict(width=2),
            marker=dict(size=8) if is_combined else dict(size=6),
            hovertemplate=f'<b>{display_name}</b><br>Iteration: %{{x}}<br>Score: %{{y:.3f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Score Trends",
        xaxis_title="Iteration",
        yaxis_title="Score",
        yaxis=dict(range=[0, 1.05]),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )
    
    return fig


def render_sidebar(refinements_df, originals_df):
    
    # Add file information at the top of sidebar
    st.sidebar.markdown("### 📁 File Information")
    st.sidebar.markdown(f"""Refinements File:  
                        **{refinements_file}**""")
    
    # Count unique examples
    unique_examples = refinements_df["example_id"].nunique()
    st.sidebar.markdown(f"""Total Examples:  
                        **{unique_examples}**""")
    
    # Example navigation buttons
    st.sidebar.html("<hr style='border: 1px solid #555; margin: 0;'>")
    st.sidebar.markdown("### 🔄 Navigate Examples")
    st.sidebar.markdown("Select an example to view:")
    examples_ids = refinements_df["example_id"].unique()
    
    # Initialize example_index if not exists
    if "example_index" not in st.session_state:
        st.session_state.example_index = 0
    
    # Create navigation buttons
    col1, col2, _ = st.sidebar.columns(3)
    with col1:
        prev_example_clicked = st.button("⬅️ Prev", key="prev_example_button")
    with col2:
        next_example_clicked = st.button("Next ➡️", key="next_example_button")
    
    # Handle navigation
    if prev_example_clicked and st.session_state.example_index > 0:
        navigate_examples(refinements_df, originals_df, "prev")
    elif next_example_clicked and st.session_state.example_index < len(examples_ids) - 1:
        navigate_examples(refinements_df, originals_df, "next")
    
    # Show current example info
    
    # Dropdown for direct selection
    selected_example_id = st.sidebar.selectbox("Or jump to:", examples_ids, index=st.session_state.example_index)

    if selected_example_id != st.session_state.example_id:
        # Update example_index to match selected example
        st.session_state.example_index = list(examples_ids).index(selected_example_id)
        select_example(refinements_df, originals_df, selected_example_id)

    st.sidebar.html("<hr style='border: 1px solid #555; margin: 0;'>")
    st.sidebar.markdown("### 📁 Example Details")
    row = st.session_state.iteration_row
    st.sidebar.markdown(f"""Title:  
                        **{row['title']}**""")
    st.sidebar.markdown(f"""Profession:  
                        **{row['profession']}**""")
    st.sidebar.markdown(f"""Purpose:  
                        **{row['purpose']}**""")
    st.sidebar.markdown(f"""Original ID:  
                        **{row['original_id']}**""")


def render_text_comparison():

    example_df = st.session_state.example_df
    row = st.session_state.iteration_row
    original_text = st.session_state.original_text
    iteration_idx = st.session_state.iteration_idx

    st.markdown("### 📄 Text Comparison")

    st.text_area("📝 Original Text", original_text, height=280, label_visibility="visible", disabled=True)
    
    iteration = row["iteration_number"]
    is_final = row["is_final_iteration"]

    # Determine previous output and label
    if iteration == 1:
        prev_output = original_text
        prev_label = "### 📝 Original Text"
    elif iteration_idx > 0:
        prev_output = example_df.iloc[iteration_idx - 1]["output"]
        prev_label = f"### ⬅️ Iteration {iteration - 1}"
    else:
        prev_output = "_Unavailable_"
        prev_label = "### ⬅️ Unknown"

    # Current output and label
    curr_output = row["output"]
    curr_label = f"### ✅ Iteration {iteration}"

    # Render side-by-side comparison
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(prev_label)
        st.markdown(prev_output or "_No output_")
    with col2:
        st.markdown(curr_label)
        st.markdown(curr_output or "_No output_")

    # Render diff viewer
    st.markdown("### 🔍 Diff: previous → current")
    if prev_output not in (None, "_Unavailable_") and curr_output:
        diff_viewer(prev_output, curr_output, split_view=True)
    else:
        st.info("Diff unavailable for this iteration.")


def render_scores_and_trends():

    example_df = st.session_state.example_df
    row = st.session_state.iteration_row

    true_best = example_df.iloc[-1]
    best_score = true_best["current_best_score"]
    best_iteration = true_best["current_best_iteration"]
    
    t_1, t_2, t_3 = st.columns(3)
    with t_1:
        st.markdown("### 🧮 Scores & Trends")
    with t_3:
        st.markdown("<div style='padding-top: 0.5rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"""#### Best Score (iteration {int(best_iteration)}): **{best_score:.3f}**""")
        
    left_col, right_col = st.columns([3, 2])

    with left_col:
        # Top row: judge score metrics
        st.markdown("<div style='padding-top: 2.2rem;'></div>", unsafe_allow_html=True)
        score_boxes = st.columns(4)
        score_boxes[0].metric("Structure", row["structure_score"], help=row["structure_reasoning"])
        score_boxes[1].metric("Coverage", row["coverage_score"], help=row["coverage_reasoning"])
        score_boxes[2].metric("Focus", row["focus_relevance_score"], help=row["focus_relevance_reasoning"])
        score_boxes[3].metric("Redundancy", row["redundancy_score"], help=row["redundancy_reasoning"])

        st.markdown("<div style='padding-top: 1rem;'></div>", unsafe_allow_html=True)
        c_s, b_s, _, _ = st.columns(4)
        with c_s:
            st.markdown(f"""Combined Score:  
                        **{row['combined_score']:.3f}**""")
        # with b_s:
        #     st.markdown(f"""Best Score (iteration {int(best_iteration)}):  
        #                 **{best_score:.3f}**""")

        # st.markdown("<div style='padding-top: 1rem;'></div>", unsafe_allow_html=True)
        # st.markdown(f"Best Score: **{best_score:.3f}** (iteration {int(best_iteration)})")
        # st.markdown(f"Best Score: **{best_score:.3f}** (iteration {int(best_iteration)})")
        st.markdown("<div style='padding-top: 1rem;'></div>", unsafe_allow_html=True)
        r_l, o_l, _, _ = st.columns(4)
        with r_l:
            # st.markdown("<div style='padding-top: 1rem;'></div>", unsafe_allow_html=True)
            st.markdown(f"""Refinement Text Length:  
                        **{st.session_state.iteration_text_length}**""")
        with o_l:
            # st.markdown("<div style='padding-top: 1rem;'></div>", unsafe_allow_html=True)
            st.markdown(f"""Original Text Length:  
                        **{row['original_text_length']}**""")

    with right_col:
        # Create and display interactive score plot
        fig = create_interactive_score_plot(example_df)
        st.plotly_chart(fig, use_container_width=True)


def render_feedback_and_reasoning():
    
    row = st.session_state.iteration_row

    combined_feedback = row.get("combined_feedback")
    if combined_feedback and not (isinstance(combined_feedback, float) and math.isnan(combined_feedback)):
        st.markdown("### 💬 Combined Feedback")
        st.write(row["combined_feedback"])

    refinement_reasoning = row.get("refinement_reasoning")
    if refinement_reasoning and not (isinstance(refinement_reasoning, float) and math.isnan(refinement_reasoning)):
        st.markdown("### 🧠 Refinement Reasoning")
        st.write(row["refinement_reasoning"])


def alter_css():

    st.markdown("""
    <style>
    [data-testid="stSidebarHeader"] {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    refinements_df, originals_df = load_data()
    st.set_page_config(layout="wide")

    select_example(refinements_df, originals_df)


    render_sidebar(refinements_df, originals_df)
    render_navigation()
    render_scores_and_trends()
    render_feedback_and_reasoning()
    render_text_comparison()
    alter_css()


if __name__ == "__main__":
    main()
