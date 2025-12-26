from flask import Flask, render_template, request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    sentiment = ""
    sentiment_emoji = ""
    user_name = ""
    text = ""

    if request.method == "POST":
        text = request.form.get("opinion", "").strip()
        user_name = request.form.get("name", "").strip()

        if text:  # Ensure text is not empty
            sid = SentimentIntensityAnalyzer()
            scores = sid.polarity_scores(text)
            compound = scores['compound']
            if compound >= 0.05:
                sentiment = "Positive"
                sentiment_emoji = "👍"
            elif compound <= -0.05:
                sentiment = "Negative"
                sentiment_emoji = "👎"
            else:
                sentiment = "Neutral"
                sentiment_emoji = "😐"
        else:
            sentiment = "Please enter a valid opinion."
            sentiment_emoji = ""

    return render_template("index.html",
                           sentiment=sentiment,
                           emoji=sentiment_emoji,
                           name=user_name,
                           text=text)

if __name__ == "__main__":
    app.run(debug=True)

