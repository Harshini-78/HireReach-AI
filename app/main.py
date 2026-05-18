import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


# Page configuration
st.set_page_config(
    layout="wide",
    page_title="HireReach AI",
    page_icon="📧"
)


def create_streamlit_app(llm, portfolio, clean_text):

    st.title("📧 HireReach AI")
    st.markdown("### AI-Powered Cold Email Generation Platform")

    url_input = st.text_input(
        "Enter a Career Page URL:",
        value="https://jobs.nike.com/job/R-33460"
    )

    submit_button = st.button("Generate Emails")

    if submit_button:

        try:
            loader = WebBaseLoader([url_input])

            data = clean_text(
                loader.load().pop().page_content
            )

            portfolio.load_portfolio()

            jobs = llm.extract_jobs(data)

            for i, job in enumerate(jobs):

                skills = job.get('skills', [])

                links = portfolio.query_links(skills)

                email = llm.write_mail(job, links)

                with st.expander(f"📌 Job {i+1}: {job.get('role', 'Job Role')}"):

                    st.write("### Extracted Job Details")
                    st.json(job)

                    st.write("### Generated Cold Email")
                    st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":

    chain = Chain()

    portfolio = Portfolio()

    create_streamlit_app(
        chain,
        portfolio,
        clean_text
    )