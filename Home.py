import streamlit as st

st.set_page_config(
    page_title="VAMA AI",
    page_icon="🔗",
)

st.write("# Welcome to Vama AI! 👋")

st.sidebar.success("Select a CSV file type you want to process. Right click and open in new tab.")

st.markdown(
    """
    VAMA AI is an LLM based webapp built specifically for
    classification of data generated as either Audio files or Chat files stored in csv format.\n
    **👈 Select csv type from the sidebar** and upload csv file\n
    Columns of csv file must remain the same as decided initially.\n
    Do NOT close the tab during processing. 
    ** Download button shows up after 100% progress completed.**
    ### For Code?
    - Check out [https://github.com/alter-sachin/vama_ai]
"""
)