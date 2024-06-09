import praw
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from time import sleep
from flask import Flask, request, render_template
import wikipedia
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # This tells Matplotlib to use a non-interactive backend
import os
import uuid
import requests


# Reddit API Credentials
client_id = "--"
client_secret = "--"
user_agent = "--"

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    stop_words = set(stopwords.words("english"))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

def analyze_sentiment(text):
    vader = SentimentIntensityAnalyzer()
    scores = vader.polarity_scores(text)
    return scores['compound']

def collect_reddit_posts(subreddit, celebrity, limit=10, delay=1, time_filter="month"):
    submissions = []
    for submission in subreddit.search(query=celebrity, time_filter=time_filter, limit=limit):
        try:
            submission.comments.replace_more(limit=3)
            for comment in submission.comments.list():
                submissions.append(clean_text(comment.body))
            sleep(delay)
        except praw.exceptions.APIException as e:
            print(f"API Error: {e}")
            break
    return submissions  # Return both lists



def analyze_trend(celebrity, subreddit_name="all"):
    subreddit = reddit.subreddit(subreddit_name)

    time_filters = ["week", "month", "year", "all"]
    time_labels = ["Last Week", "Last Month", "Last Year", "All Time"]

    sentiment_scores = []
    for time_filter in time_filters:
        posts = collect_reddit_posts(subreddit, celebrity, time_filter=time_filter)
        if posts:
            sentiment_scores.append(sum([analyze_sentiment(text) for text in posts]) / len(posts))
        else:
            sentiment_scores.append(0)  # Default to neutral if no posts

    plt.figure(figsize=(10, 6))
    plt.plot(time_labels, sentiment_scores, marker='o')
    plt.title(f"Sentiment Trend for '{celebrity}' on Reddit")
    plt.xlabel("Time Period")
    plt.ylabel("Average Sentiment Score")
    plt.ylim(-1, 1)
    plt.xticks(range(len(time_labels)), time_labels)

    # Save the plot with a unique filename
    chart_filename = f"trend_{celebrity}_{uuid.uuid4()}.png"  # Unique filename using UUID
    chart_path = os.path.join(app.static_folder, chart_filename)
    plt.savefig(chart_path,transparent=True)
    plt.close()  # Close the figure after saving

    return chart_filename  # Return the filename

def analyze_sentiment_distribution(celebrity, subreddit_name="all", time_labels = ["Last Week", "Last Month", "Last Year", "All Time"]):
    subreddit = reddit.subreddit(subreddit_name)
    time_filters = ["week", "month", "year", "all"]
    positive_counts = []
    negative_counts = []
    neutral_counts = []

    for time_filter in time_filters:
        posts = collect_reddit_posts(subreddit, celebrity, time_filter=time_filter)
        if posts:
            sentiment_scores = [analyze_sentiment(text) for text in posts]
            positive_counts.append(sum(1 for score in sentiment_scores if score > 0.05))
            negative_counts.append(sum(1 for score in sentiment_scores if score < -0.05))
            neutral_counts.append(len(sentiment_scores) - positive_counts[-1] - negative_counts[-1])
        else:
            positive_counts.append(0)
            negative_counts.append(0)
            neutral_counts.append(0)

    # Plotting the sentiment distribution
    plt.figure(figsize=(10, 6))
    plt.stackplot(time_labels, positive_counts, negative_counts, neutral_counts, 
                  labels=['Positive', 'Negative', 'Neutral'], colors=['#64c45a', '#C9190B', '#A2D9D9'], alpha=0.7)
    plt.title(f"Sentiment Distribution for '{celebrity}' on Reddit")
    plt.xlabel("Time Period")
    plt.ylabel("Number of Comments")
    plt.legend(loc='upper left')

    # Save the distribution chart
    distribution_chart_filename = f"distribution_{celebrity}_{uuid.uuid4()}.png"
    distribution_chart_path = os.path.join(app.static_folder, distribution_chart_filename)
    plt.savefig(distribution_chart_path, transparent=True)
    plt.close()

    return distribution_chart_filename


def analyze_reddit_sentiment(celebrity): 
    subreddit_name = "all"

    subreddit = reddit.subreddit(subreddit_name)
    posts= collect_reddit_posts(subreddit, celebrity)

    sentiment_scores = [analyze_sentiment(text) for text in posts]
    positive_count = sum(1 for score in sentiment_scores if score > 0.05)
    negative_count = sum(1 for score in sentiment_scores if score < -0.05)
    neutral_count = len(sentiment_scores) - positive_count - negative_count

    total_posts = len(posts)
    if total_posts == 0:
        return 0, None  # Handle the case where no posts are found

    positive_percentage = (positive_count / total_posts) * 100
    negative_percentage = (negative_count / total_posts) * 100
    neutral_percentage = (neutral_count / total_posts) * 100

    # Create pie chart for sentiment breakdown
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive_percentage, negative_percentage, neutral_percentage]
    colors = ['#64c45a', '#C9190B', '#A2D9D9']  

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140,labeldistance=0.4, pctdistance=0.85)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f"Sentiment Breakdown for {celebrity}")

    # Save the pie chart
    pie_chart_filename = f"pie_chart_{celebrity}_{uuid.uuid4()}.png"
    pie_chart_path = os.path.join(app.static_folder, pie_chart_filename)
    plt.savefig(pie_chart_path, transparent=True)
    plt.close()


    average_score = sum(sentiment_scores) / len(sentiment_scores)
    return average_score, pie_chart_filename



# Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/analyze', methods=['POST'])
def analyze_sentiment_endpoint():
    celebrity = request.form['name']

    try:
        average_score, pie_chart = analyze_reddit_sentiment(celebrity)
        if average_score == 0:
            return "No data found for this celebrity"
        sentiment = "Positive" if average_score > 0.05 else "Negative" if average_score < -0.05 else "Neutral"

        wikipedia_summary = wikipedia.summary(celebrity, sentences=3)
        wikipedia_image_url = wikipedia.page(celebrity).images[0]

        trend_chart_path = analyze_trend(celebrity)
        distribution_chart = analyze_sentiment_distribution(celebrity) #get the filename

    except wikipedia.exceptions.PageError:
        wikipedia_summary = "No Wikipedia page found."
        wikipedia_image_url = None
        trend_chart_path = None
        pie_chart = None
        distribution_chart= None
    except wikipedia.exceptions.DisambiguationError as e:
        wikipedia_summary = f"Multiple people found. Please refine your search. Options: {e.options}"
        wikipedia_image_url = None
        trend_chart_path = None
        pie_chart = None
        distribution_chart= None


    return render_template('result.html', sentiment=sentiment,
                                         summary=wikipedia_summary,
                                         image_url=wikipedia_image_url,
                                         trend_chart=trend_chart_path,
                                         pie_chart=pie_chart,
                                         distribution_chart=distribution_chart  # Pass distribution chart filename
)


if __name__ == '__main__':
    app.run(debug=True)
