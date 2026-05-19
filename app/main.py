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
    # Custom CSS for Modern Light SaaS Theme
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
        }
        
        .stApp {
            background-color: #f8fafc;
            background-image: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.05) 0%, rgba(248, 250, 252, 1) 70%);
            background-attachment: fixed;
        }

        /* Hide Streamlit Header/Footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Layout overrides for centering and width */
        .block-container {
            max-width: 900px !important;
            padding-top: 3rem !important;
            padding-bottom: 3rem !important;
        }

        /* Hero Section */
        .hero-container {
            text-align: center;
            margin-bottom: 3rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            animation: fadeIn 0.8s ease-out;
        }
        .hero-logo-box {
            background: linear-gradient(135deg, #6366f1, #a855f7);
            width: 56px;
            height: 56px;
            border-radius: 14px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.8rem;
            font-weight: 700;
            color: white;
            margin-bottom: 1.2rem;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.5);
        }
        .hero-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            color: #0f172a;
            letter-spacing: -0.5px;
            line-height: 1.2;
        }
        .hero-title span {
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            font-weight: 400;
            color: #64748b;
            margin-top: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .hero-tagline-pill {
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(226, 232, 240, 1);
            padding: 0.5rem 1.2rem;
            border-radius: 50px;
            font-size: 0.85rem;
            color: #475569;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            backdrop-filter: blur(8px);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        }

        /* Streamlit Input Overrides */
        div[data-testid="stTextInput"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
            margin-bottom: 1rem;
        }
        div[data-testid="stTextInput"] label {
            color: #334155 !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
        }
        div[data-baseweb="input"] {
            background-color: #f8fafc !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            transition: all 0.2s ease;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
            background-color: #ffffff !important;
        }
        div[data-baseweb="input"] input {
            color: #0f172a !important;
            font-size: 1rem !important;
            padding: 0.8rem 1rem !important;
        }
        div[data-baseweb="input"] input::placeholder {
            color: #94a3b8 !important;
            opacity: 1 !important;
        }

        /* Button override */
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
            margin-bottom: 3rem;
        }
        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            color: white !important;
            border: none !important;
            padding: 0.8rem 2.5rem !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            border-radius: 50px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 6px 15px rgba(99, 102, 241, 0.2) !important;
            width: auto !important;
        }
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3) !important;
            background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        }
        div[data-testid="stButton"] > button:active {
            transform: translateY(0) !important;
        }

        /* Feature Cards */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.2rem;
            margin-top: 2rem;
            margin-bottom: 4rem;
        }
        @media (min-width: 768px) {
            .features-grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }
        .feature-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.5rem 1rem;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
        }
        .feature-card:hover {
            border-color: #cbd5e1;
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        }
        .feature-icon {
            font-size: 1.6rem;
            margin-bottom: 0.8rem;
        }
        .feature-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0.4rem;
        }
        .feature-desc {
            font-size: 0.8rem;
            color: #64748b;
            line-height: 1.5;
        }

        /* Expander and Results Customization */
        div[data-testid="stExpander"] {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
        }
        div[data-testid="stExpander"] > details > summary {
            background-color: #f8fafc !important;
            padding: 1rem 1.5rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #0f172a !important;
            border-bottom: 1px solid #e2e8f0 !important;
        }
        div[data-testid="stExpander"] > details > summary:hover {
            color: #6366f1 !important;
            background-color: #f1f5f9 !important;
        }
        div[data-testid="stExpanderDetails"] {
            padding: 1.5rem !important;
            background-color: #ffffff !important;
        }

        /* JSON and Code blocks */
        .stCodeBlock, .stJson {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }

        /* Footer */
        .footer-container {
            display: flex;
            justify-content: center;
            margin-top: 4rem;
        }
        .footer-pill {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 0.6rem 1.5rem;
            border-radius: 50px;
            font-size: 0.8rem;
            color: #64748b;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="hero-container">
            <div class="hero-logo-box">@</div>
            <h1 class="hero-title">HireReach <span>AI</span></h1>
            <div class="hero-subtitle">Intelligent Cold Email Generation</div>
            <div class="hero-tagline-pill">
                <span style="color: #6366f1;">✦</span> Smart Outreach • Semantic Matching • Fast Execution
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Input Section
    url_input = st.text_input(
        "🔗 Enter a Career Page URL",
        value="https://jobs.nike.com/job/R-33460",
        placeholder="e.g. https://company.com/careers/job-id"
    )
    
    submit_button = st.button("🚀 Generate Email")

    # Features Section
    st.markdown("""
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon" style="color: #8b5cf6;">🧠</div>
                <div class="feature-title">AI Extraction</div>
                <div class="feature-desc">Intelligently parses job roles and requirements.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon" style="color: #0ea5e9;">🔍</div>
                <div class="feature-title">Semantic Match</div>
                <div class="feature-desc">Finds exact portfolio matches via vector search.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon" style="color: #6366f1;">✉️</div>
                <div class="feature-title">Custom Outreach</div>
                <div class="feature-desc">Writes emails tailored to the job description.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon" style="color: #f59e0b;">⚡</div>
                <div class="feature-title">Lightning Fast</div>
                <div class="feature-desc">Powered by Groq inference for instant results.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Output Section
    if submit_button:
        st.markdown("<hr style='border-color: #e2e8f0; margin: 2rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #0f172a; margin-bottom: 2rem;'>✨ Generated Output</h3>", unsafe_allow_html=True)
        
        with st.spinner("🧠 Analyzing page and generating personalized email..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                for i, job in enumerate(jobs):
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)

                    with st.expander(f"📌 Found Job {i+1}: {job.get('role', 'Job Role')}", expanded=True):
                        
                        st.markdown("<h4 style='color: #6366f1; font-size: 1rem; margin-top: 0;'>📊 Extracted Data</h4>", unsafe_allow_html=True)
                        st.json(job)

                        st.markdown("<h4 style='color: #6366f1; font-size: 1rem; margin-top: 1.5rem;'>✉️ Generated Email</h4>", unsafe_allow_html=True)
                        st.code(email, language='markdown')

            except Exception as e:
                st.error(f"An Error Occurred: {e}")

    # Footer
    st.markdown("""
        <div class="footer-container">
            <div class="footer-pill">
                Built with Groq • LangChain • ChromaDB • Streamlit 💜
            </div>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":

    chain = Chain()

    portfolio = Portfolio()

    create_streamlit_app(
        chain,
        portfolio,
        clean_text
    )