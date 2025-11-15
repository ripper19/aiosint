import streamlit as st

def display(target, data, report):
    st.title("osint threat ai")
    st.subheader(f"Target: {target}")
    st.json(data)
    st.markdown("### AI Risk Sumamry")
    st.write(report)
