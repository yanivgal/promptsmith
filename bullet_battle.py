import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("bulletized_results.csv")

# Select example
selected_index = st.selectbox("select text:", df.index, format_func=lambda i: f"Example {i+1}")

st.text_area("original text", df.loc[selected_index, "text"], height=200, key="original_text", label_visibility="visible")

# Show original and bulletized versions
st.text_area("original text", df.loc[selected_index, "text"], height=150)
col1, col2 = st.columns(2)
with col1:
    st.text_area("bulletized v1", df.loc[selected_index, "simple_bullets"], height=200)
with col2:
    st.text_area("bulletized v2", df.loc[selected_index, "better_bullets"], height=200)

# Evaluation
choice = st.radio("",
    ["v1 is better", "v2 is better", "both are bad"],
    horizontal=True
)

# Optional reason
reason = st.text_area("reason:")

# Submit
if st.button("submit"):
    st.success(f"You selected: {choice}")
    if reason:
        st.write("Reason:", reason)
