import streamlit as st
from backend import predict_sentiment

# Page setup
st.set_page_config(
    page_title="IMDB Sentiment Analyzer",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 IMDB Movie Review Sentiment Analyzer")

st.write(
    "Enter a movie review below or click on a sample review to test if our CNN model "
    "predicts it as **Positive** or **Negative**."
)

# Initialize Session State for review input
if "review_text" not in st.session_state:
    st.session_state["review_text"] = ""

# Sample reviews
positive_reviews = [
    "This movie was absolutely amazing. The story was engaging and the acting was excellent.",
    "I loved this film! The characters were interesting and the ending was very satisfying.",
    "One of the best movies I have watched in a long time. Brilliant performances."
]

negative_reviews = [
    "This movie was extremely boring. The story was weak and the acting was disappointing.",
    "I really disliked this film. The characters were poorly written and the plot made no sense.",
    "A complete waste of time. The movie was slow, predictable, and not entertaining."
]

# Display sample reviews in two columns with interactive copy buttons
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 Positive Sample Reviews")
    for i, p_review in enumerate(positive_reviews, 1):
        st.info(f"**Positive Review {i}**\n\n{p_review}")
        if st.button(f"📋 Use Positive Sample {i}", key=f"pos_{i}"):
            st.session_state["review_text"] = p_review

with col2:
    st.subheader("🔴 Negative Sample Reviews")
    for i, n_review in enumerate(negative_reviews, 1):
        st.error(f"**Negative Review {i}**\n\n{n_review}")
        if st.button(f"📋 Use Negative Sample {i}", key=f"neg_{i}"):
            st.session_state["review_text"] = n_review

st.divider()

st.subheader("📝 Enter Your Own Review")

# Text area bound with session state
review = st.text_area(
    "Movie Review:",
    value=st.session_state["review_text"],
    height=150,
    placeholder="Example: This movie was amazing and I really enjoyed it!",
    key="review_input"
)

# Action button
if st.button("🔍 Check Sentiment", type="primary"):

    if not review.strip():
        st.warning("⚠️ Please enter a review or select a sample review above.")

    else:
        with st.spinner("Analyzing sentiment... Please wait ⏳"):
            try:
                sentiment, confidence = predict_sentiment(review)

                st.markdown("---")
                st.subheader("🎯 Prediction Result")

                res_col1, res_col2 = st.columns([1, 2])

                with res_col1:
                    if sentiment == "Positive":
                        st.success("😊 **POSITIVE REVIEW**")
                    else:
                        st.error("😞 **NEGATIVE REVIEW**")

                with res_col2:
                    st.metric(label="Confidence Score", value=f"{confidence:.2f}%")

            except Exception as e:
                st.error("❌ Prediction error occurred.")
                st.exception(e)