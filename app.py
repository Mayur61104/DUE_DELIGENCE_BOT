import streamlit as st
from backend import generate

st.set_page_config(
    page_title="Due Diligence Copilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Due Diligence Copilot")

st.write(
    "Generate AI-powered company due diligence reports."
)

with st.sidebar:

    st.header("About")

    st.write("""
    AI-powered Due Diligence Tool
    """)

company = st.text_input(
    "Company Name",
    placeholder="NVIDIA"
)

if st.button("Generate Report"):

    if company.strip() == "":

        st.warning("Please enter a company name.")

    else:

        with st.spinner("Performing due diligence... (please wait may take 20-40 secs"):

            report = generate(company)

        st.success("Report Generated")

        st.markdown(report)

        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name=f"{company}_report.txt",
            mime="text/plain"
        )
