<h1 align="center" id="title">Reddit Celebrity Sentiment Analysis Tool</h1>

<p id="description">This Flask-based web application analyzes public sentiment towards celebrities on Reddit. It provides a user-friendly interface to search for a celebrity and get insights.</p>

<h2>Project Screenshots:</h2>

<img src="https://github.com/muhamad-bilal/RentiAnalyzer/blob/main/static/ss1.png" alt="project-screenshot" width="auto" height="auto">

<img src="https://github.com/muhamad-bilal/RentiAnalyzer/blob/main/static/ss2.png" alt="project-screenshot" width="auto" height="auto">

<img src="https://github.com/muhamad-bilal/RentiAnalyzer/blob/main/static/ss3.png" alt="project-screenshot" width="auto" height="auto">

<img src="https://github.com/muhamad-bilal/RentiAnalyzer/blob/main/static/ss4.png" alt="project-screenshot" width="auto" height="auto">

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Reddit Data Collection: Fetches recent comments from the "all" subreddit (or a specified subreddit) related to the celebrity.
*   Sentiment Analysis: Uses the VADER (Valence Aware Dictionary and sentiment Reasoner) sentiment analysis tool to calculate sentiment scores for each comment.
*   Trend Analysis: Generates a line graph to visualize how average sentiment changes over different time periods.
*   Sentiment Distribution: Creates a pie chart to show the proportion of positive negative and neutral comments.
*   Sentiment Distribution Over Time: Illustrates how the proportion of each sentiment category changes across different time periods providing insight into shifts in public opinion.
*   Wikipedia Integration: Fetches a summary and image of the celebrity from Wikipedia for additional context.
*   Error Handling: Includes error handling for cases where no data is found or the API encounters issues.
*   User-friendly Interface: A simple web interface for entering celebrity names and viewing results.

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the Repository:</p>

```
git clone https://github.com/muhamad-bilal/RentiAnalyzer.git 
```

<p>2. Install Dependencies:</p>

```
pip install -r requirements.txt
```

<p>3. Get Reddit API Credentials:</p>

```
https://www.reddit.com/prefs/apps
```

<p>4. Run the App:</p>

```
python app.py
```

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Python
*   Flask
*   PRAW(Python Reddit API Wrapper)
*   Matplotlib
*   NLTK (Natural Language Toolkit)
*   VADER SentimentIntensityAnalyzer
*   Wikipedia API (Wikipedia Package)
*   HTML
*   CSS
*   JavaScript
