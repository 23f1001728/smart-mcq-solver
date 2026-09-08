import streamlit as st
import joblib
from html import escape

st.set_page_config(
    page_title="Smart MCQ Solver | Ranked answers",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #182230;
        --muted: #697586;
        --line: #e7e9ee;
        --blue: #2563eb;
        --blue-soft: #eef4ff;
        --gold: #d48a18;
    }

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: 0 !important; }
    .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 4rem; }
    [data-testid="stSidebar"] { background: #f7f8fb; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: var(--muted); }
    .hero { padding: 1.2rem 0 1.8rem; border-bottom: 1px solid var(--line); margin-bottom: 1.8rem; }
    .eyebrow { color: var(--blue); font-size: .75rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
    .developer-link { align-items: center; color: var(--blue); display: inline-flex; gap: .45rem; text-decoration: none; }
    .developer-link:hover { text-decoration: underline; }
    .github-icon { height: 1.05rem; width: 1.05rem; }
    .hero h1 { font-size: clamp(2rem, 4vw, 3.5rem); line-height: 1.05; margin: .35rem 0 .7rem; }
    .hero p { color: var(--muted); font-size: 1.05rem; max-width: 660px; margin: 0; }
    .section-label { color: var(--ink); font-size: 1.08rem; font-weight: 700; margin: .3rem 0 .8rem; }
    .option-label { color: var(--blue); font-family: 'Space Grotesk', sans-serif; font-weight: 700; }
    .answer-card { background: linear-gradient(135deg, #f5f8ff 0%, #ffffff 78%); border: 1px solid #dbe6ff; border-left: 5px solid var(--blue); border-radius: 10px; padding: 1.2rem 1.35rem; margin: .6rem 0 1.3rem; }
    .answer-card .kicker { color: var(--blue); font-size: .76rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
    .answer-card .answer { color: var(--ink); font-family: 'Space Grotesk', sans-serif; font-size: 1.55rem; font-weight: 700; margin: .3rem 0; }
    .answer-card .confidence { color: var(--muted); font-size: .92rem; }
    .rank-card { border: 1px solid var(--line); border-radius: 10px; padding: 1rem 1.1rem .75rem; min-height: 150px; background: white; }
    .rank-card .rank { color: var(--gold); font-weight: 700; font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; }
    .rank-card .label { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 700; margin: .25rem 0 .4rem; }
    .rank-card .text { color: #4b5563; min-height: 2.8rem; }
    .hint { background: #f8fafc; border: 1px solid var(--line); border-radius: 8px; padding: .75rem 1rem; color: var(--muted); font-size: .9rem; }
    div.stButton > button { border-radius: 8px; font-weight: 600; min-height: 2.8rem; }

    @media (prefers-color-scheme: dark) {
        :root {
            --ink: #f3f6fb;
            --muted: #b4bfce;
            --line: #344052;
            --blue: #82adff;
            --blue-soft: #1d3154;
            --gold: #f1b84b;
        }
        [data-testid="stSidebar"] { background: #111923; border-right-color: var(--line); }
        .hero p, [data-testid="stCaptionContainer"], [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: var(--muted); }
        .hero { border-bottom-color: var(--line); }
        .answer-card { background: #17243a; border-color: #355b99; }
        .answer-card .answer, .section-label { color: var(--ink); }
        .rank-card { background: #18202c; border-color: var(--line); }
        .rank-card .text { color: #c4cedb; }
        .hint { background: #18202c; border-color: var(--line); color: var(--muted); }
    }

    [data-theme="dark"] {
        --ink: #f3f6fb;
        --muted: #b4bfce;
        --line: #344052;
        --blue: #82adff;
        --blue-soft: #1d3154;
        --gold: #f1b84b;
    }
    [data-theme="dark"] [data-testid="stSidebar"] { background: #111923; border-right-color: var(--line); }
    [data-theme="dark"] .hero p,
    [data-theme="dark"] [data-testid="stCaptionContainer"],
    [data-theme="dark"] [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: var(--muted); }
    [data-theme="dark"] .hero { border-bottom-color: var(--line); }
    [data-theme="dark"] .answer-card { background: #17243a; border-color: #355b99; }
    [data-theme="dark"] .answer-card .answer,
    [data-theme="dark"] .section-label { color: var(--ink); }
    [data-theme="dark"] .rank-card { background: #18202c; border-color: var(--line); }
    [data-theme="dark"] .rank-card .text { color: #c4cedb; }
    [data-theme="dark"] .hint { background: #18202c; border-color: var(--line); color: var(--muted); }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <a class="eyebrow developer-link" href="https://github.com/Reflex-Angle" title="Meet the developer">
            Meet the developer
            <svg class="github-icon" viewBox="0 0 24 24" aria-hidden="true">
                <path fill="currentColor" d="M12 .5a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.75.08-.74.08-.74 1.2.09 1.84 1.23 1.84 1.23 1.07 1.84 2.8 1.31 3.49 1 .11-.78.42-1.31.76-1.61-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.23-3.22-.12-.3-.53-1.52.12-3.18 0 0 1-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.3-1.55 3.3-1.23 3.3-1.23.65 1.66.24 2.88.12 3.18.77.84 1.23 1.91 1.23 3.22 0 4.61-2.8 5.62-5.48 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.22.69.83.57A12 12 0 0 0 12 .5Z"/>
            </svg>
        </a>
        <h1>Smart MCQ Solver</h1>
        <p>Turn a question and five choices into a ranked shortlist. Get a fast and transparent ranking to assist your decision.</p>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("## About the solver")
    st.write("A TF-IDF + logistic regression classifier ranks the five answer choices from most to least likely.")
    st.divider()
    st.markdown("**Output**")
    st.caption("Top 3 choices with probability scores")
    st.markdown("**Input format**")
    st.caption("One question and exactly five answer options")
    st.divider()
    st.caption("Tip: include the full question context and keep each option concise.")

left_intro, right_intro = st.columns([3, 1])
with left_intro:
    st.markdown('<div class="section-label">Build your question</div>', unsafe_allow_html=True)


@st.cache_resource
def load_model():
    model = joblib.load("lr_model.joblib")
    vectorizer = joblib.load("tfidf_vectorizer.joblib")
    label_encoder = joblib.load("label_encoder.joblib")

    return model, vectorizer, label_encoder


model, vectorizer, label_encoder = load_model()

question = st.text_area(
    "Question",
    placeholder="Paste the complete question here...",
    height=125,
    help="Include enough context for the model to compare the answer choices."
)

st.markdown('<div class="section-label">Answer options</div>', unsafe_allow_html=True)

option_columns = st.columns(5)
option_a = option_columns[0].text_input("A", placeholder="Option A", key="option_a")
option_b = option_columns[1].text_input("B", placeholder="Option B", key="option_b")
option_c = option_columns[2].text_input("C", placeholder="Option C", key="option_c")
option_d = option_columns[3].text_input("D", placeholder="Option D", key="option_d")
option_e = option_columns[4].text_input("E", placeholder="Option E", key="option_e")

st.markdown('<div class="hint">The ranking is based on the confidence scores of a linguistic model, it does not substitute for understanding the underlying concept.</div>', unsafe_allow_html=True)
st.write("")
predict_button = st.button("Rank answer choices", type="primary", use_container_width=True)


if predict_button:

    if not all([
        question,
        option_a,
        option_b,
        option_c,
        option_d,
        option_e
    ]):
        st.warning(
            "Please enter the question and all five answer options."
        )

    else:

        combined_text = (
            f"Question: {question}\n\n"
            f"A. {option_a}\n"
            f"B. {option_b}\n"
            f"C. {option_c}\n"
            f"D. {option_d}\n"
            f"E. {option_e}"
        )

        input_vector = vectorizer.transform([combined_text])

        probabilities = model.predict_proba(input_vector)[0]

        top3_indices = probabilities.argsort()[::-1][:3]

        top3_labels = label_encoder.inverse_transform(top3_indices)


        option_texts = {
            "A": option_a,
            "B": option_b,
            "C": option_c,
            "D": option_d,
            "E": option_e
        }


        best_label = top3_labels[0]
        best_index = top3_indices[0]

        best_answer = option_texts[best_label]
        best_confidence = probabilities[best_index] * 100

        st.divider()
        st.markdown('<div class="section-label">Best match</div>', unsafe_allow_html=True)
        st.markdown(
            f'''<div class="answer-card">
                <div class="kicker">Recommended choice</div>
                <div class="answer">Option {best_label} · {escape(best_answer)}</div>
                <div class="confidence">Model confidence: <strong>{best_confidence:.2f}%</strong></div>
            </div>''',
            unsafe_allow_html=True
        )

        st.markdown('<div class="section-label">Ranked shortlist</div>', unsafe_allow_html=True)
        rank_columns = st.columns(3)
        rank_names = ["1st place", "2nd place", "3rd place"]
        for rank, (label, index) in enumerate(zip(top3_labels, top3_indices)):
            confidence = probabilities[index] * 100
            answer_text = option_texts[label]
            with rank_columns[rank]:
                st.markdown(
                    f'''<div class="rank-card">
                        <div class="rank">{rank_names[rank]}</div>
                        <div class="label">Option {label}</div>
                        <div class="text">{escape(answer_text)}</div>
                        <div><strong>{confidence:.2f}%</strong> confidence</div>
                    </div>''',
                    unsafe_allow_html=True
                )
                st.progress(float(probabilities[index]))

        spread = (probabilities[top3_indices[0]] - probabilities[top3_indices[1]]) * 100
        st.caption(f"The leading choice is {spread:.2f} percentage points ahead of the next-ranked option.")