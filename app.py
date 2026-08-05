import streamlit as st
import joblib

st.set_page_config(
    page_title="Smart MCQ Solver",
    page_icon="📝",
    layout="centered"
)

st.title("Smart MCQ Solver")

st.write(
    "Enter a multiple-choice question and the model will "
    "predict the top 3 most likely answers."
)


@st.cache_resource
def load_model():
    model = joblib.load("lr_model.joblib")
    vectorizer = joblib.load("tfidf_vectorizer.joblib")
    label_encoder = joblib.load("label_encoder.joblib")

    return model, vectorizer, label_encoder


model, vectorizer, label_encoder = load_model()

st.subheader("Enter Question")

question = st.text_area(
    "Question",
    placeholder="Enter the MCQ question here..."
)

st.subheader("Answer Options")

option_a = st.text_input("A", placeholder="Enter option A")
option_b = st.text_input("B", placeholder="Enter option B")
option_c = st.text_input("C", placeholder="Enter option C")
option_d = st.text_input("D", placeholder="Enter option D")
option_e = st.text_input("E", placeholder="Enter option E")

predict_button = st.button(
    "Predict Answer",
    type="primary",
    use_container_width=True
)


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

        # Convert input using the trained TF-IDF vectorizer
        input_vector = vectorizer.transform([combined_text])

        # Get probability for each answer class
        probabilities = model.predict_proba(input_vector)[0]

        # Rank classes from highest to lowest probability
        top3_indices = probabilities.argsort()[::-1][:3]

        # Convert encoded classes back to A, B, C, D, E
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

        st.subheader("Predicted Answer")

        st.success(
            f"Option {best_label}: {best_answer}"
        )

        st.write(
            f"Model confidence: **{best_confidence:.2f}%**"
        )

        st.divider()

        st.subheader("Top 3 Predictions")

        medals = ["🥇", "🥈", "🥉"]

        for rank, (label, index) in enumerate(
            zip(top3_labels, top3_indices)
        ):

            confidence = probabilities[index] * 100
            answer_text = option_texts[label]

            st.markdown(
                f"### {medals[rank]} Option {label}"
            )

            st.write(answer_text)

            st.write(
                f"Confidence: **{confidence:.2f}%**"
            )

            st.progress(float(probabilities[index]))