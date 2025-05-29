import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("bulletized_results.csv")

st.set_page_config(layout="wide")

# Select example
selected_index = st.selectbox("select text:", df.index, format_func=lambda i: f"Example {i+1}")

st.text_area(
    "original text",
    df.loc[selected_index, "text"],
    height=400,
    key="original_text",
    label_visibility="visible",
)

col1, col2 = st.columns(2)
with col1:
    st.title(":blue[bulletized v1]")
    st.markdown(df.loc[selected_index, "simple_bullets"])
with col2:
    st.title(":blue[bulletized v2]")
    st.markdown(df.loc[selected_index, "better_bullets"])

# Get existing values if they exist
current_choice = df.loc[selected_index, "who_is_better"] if "who_is_better" in df.columns and pd.notna(df.loc[selected_index, "who_is_better"]) else None
current_reason = df.loc[selected_index, "reason"] if "reason" in df.columns and pd.notna(df.loc[selected_index, "reason"]) else ""

# Evaluation
choice_options = ["v1 is better", "v2 is better", "both are bad"]
# Map the stored choice to the index if it exists
choice_index = choice_options.index(current_choice) if current_choice in choice_options else 0

choice = st.radio(
    "",
    choice_options,
    index=choice_index,
    horizontal=True,
    key=f"radio_{selected_index}"
)

# choice = st.radio("",
#     ["v1 is better", "v2 is better", "both are bad"],
#     horizontal=True
# )

# Optional reason
reason = st.text_area("reason (optional):", value=current_reason)

# Submit
if st.button("submit"):
    # Update the DataFrame with the new values
    if "who_is_better" not in df.columns:
        df["who_is_better"] = None
    if "reason" not in df.columns:
        df["reason"] = ""
        
    df.loc[selected_index, "who_is_better"] = choice
    df.loc[selected_index, "reason"] = reason
    
    # Save the updated DataFrame back to CSV
    df.to_csv("bulletized_results.csv", index=False)
    
    st.success(f"You selected: {choice}")
    if reason:
        st.write("Reason:", reason)
