import streamlit as st
from backend import generate

st.set_page_config(
    page_title="Due Diligence Copilot",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("📊 Due Diligence Copilot")

st.caption(
    "AI-powered company due diligence reports using web research, financial data, and LLM analysis."
)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header("About")

    st.write("""
    **Due Diligence Copilot V1**
    
    Generate structured due diligence reports covering:
    
    - Company Overview
    - Business Model
    - Financial Overview
    - Competitive Landscape
    - Management & Leadership
    - Recent Developments
    - Opportunities
    - Risks
    - Source-backed Analysis
    """)

    st.markdown("---")

    st.write(
        "⚠️ Reports are generated using publicly available information and should be independently verified."
    )

# -----------------------------
# COMPANY SELECTION
# -----------------------------

supported_companies = [
    "NVIDIA",
    "Microsoft",
    "Amazon",
    "Apple",
    "Meta",
    "Alphabet",
    "Tesla",
    "Infosys",
    "TCS",
    "Reliance"
]

selected_company = st.selectbox(
    "Select a Company",
    ["Custom Company"] + supported_companies
)

if selected_company == "Custom Company":

    company = st.text_input(
        "Enter Company Name",
        placeholder="Example: OpenAI"
    )

else:

    company = selected_company

st.divider()

# -----------------------------
# GENERATE REPORT
# -----------------------------

if st.button(
    "🚀 Generate Due Diligence Report",
    use_container_width=True
):

    if not company or company.strip() == "":

        st.warning("Please enter a company name.")

    else:

        try:

            with st.spinner(
                "Performing due diligence... This may take 20-60 seconds."
            ):

                report = generate(company)

            st.success("Report Generated Successfully")

            st.markdown("---")
            st.subheader("Generated Report")

            st.markdown(report)

            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"{company.lower().replace(' ', '_')}_due_diligence_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:

            st.error("An error occurred while generating the report.")

            st.exception(e)
