import streamlit as st
from backend import run_model

st.set_page_config(
    page_title="characterify",
    page_icon="🎭",
    layout="centered"
)

# Title
st.markdown(
    """
    <h1 style="
        text-align: center;
        font-weight: 1500;
        letter-spacing: 3px;
    ">
     🎭 CHARACTERIFY 🎭
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:18px;'>Upload your chats and amuse yourself!</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-size:18px;'>"
    "Group project by Anuvesha, Prachi & Aditi"
    "</p>",
    unsafe_allow_html=True
)

# File uploaders
chat_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type="txt")
script_file = st.file_uploader("Upload Movie Script (.txt)", type="txt")

# Initialize results
results = {}

# Check if files are uploaded
if chat_file and script_file:
    chat_lines = chat_file.read().decode("utf-8").splitlines()
    script_lines = script_file.read().decode("utf-8").splitlines()

    if st.button("✨ Match Characters"):
        with st.spinner("Analyzing personalities..."):
            results = run_model(chat_lines, script_lines)
        st.success("Done!")

        st.markdown("## 🎯 Results")
        
        # Display results
        for person, character in results.items():
            st.markdown(
                f"""
                <div style="
                    background-color: white;
                    padding: 16px;
                    margin-bottom: 12px;
                    border-radius: 12px;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                ">
                    <h4 style="margin-bottom:6px;">👤 {person}</h4>
                    <p style="font-size:18px;">🎭 Character: <b>{character}</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )
