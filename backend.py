import tensorflow as tf
import pickle
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences


# Load CNN model
model = tf.keras.models.load_model("imdb_cnn_model.keras")


# Load tokenizer
with open("tokenizer.pkl", "rb") as file:
    tokenizer = pickle.load(file)


def clean_text(text):
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def predict_sentiment(review):

    cleaned_review = clean_text(review)

    sequence = tokenizer.texts_to_sequences([cleaned_review])

    padded = pad_sequences(
        sequence,
        maxlen=300,
        padding="post",
        truncating="post"
    )

    prediction = model.predict(padded, verbose=0)[0][0]

    if prediction >= 0.5:
        sentiment = "Positive"
        confidence = prediction * 100
    else:
        sentiment = "Negative"
        confidence = (1 - prediction) * 100

    return sentiment, confidence