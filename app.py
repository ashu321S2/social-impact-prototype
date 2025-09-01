from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def collect_data():
    """
    Collects a list of posts from a public website for a scraping example.
    Note: This is a simplified example for a prototype. The HTML structure
    may change, causing the scraper to fail.
    """
    url = "https://news.ycombinator.com/"
    headers = {
        # It's important to provide a User-Agent to avoid being blocked.
        'User-Agent': 'SocialImpactPrototype/1.0'  
    }
    print("Attempting to collect data from:", url)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = []
        # Finding all post titles on Hacker News.
        # This selector is more stable than the previous one for Reddit.
        for title_tag in soup.find_all('a', class_='titlelink'):
            posts.append(title_tag.text)
        
        print("Successfully collected posts:")
        for post in posts:
            print(f"- {post}")
            
        return posts
    except requests.exceptions.RequestException as e:
        print(f"Error collecting data: {e}")
        return []

def analyze_sentiment(text):
    """
    Performs a very simple, rule-based sentiment analysis on a string.
    In a real-world application, a more robust NLP library like NLTK or spaCy
    would be used for accurate sentiment analysis.
    """
    text = text.lower()
    negative_keywords = ['hate', 'toxic', 'unhealthy', 'misinformation', 'harmful', 'dangerous']
    if any(keyword in text for keyword in negative_keywords):
        return 'negative'
    else:
        return 'neutral'

@app.route('/')
def home():
    """
    The main route for the web application. It handles the data flow:
    1. Calls the data collection function.
    2. Analyzes the sentiment of each collected post.
    3. Renders the main dashboard template with the filtered data.
    """
    raw_posts = collect_data()
    analyzed_posts = []
    for post in raw_posts:
        sentiment = analyze_sentiment(post)
        analyzed_posts.append({
            'text': post,
            'sentiment': sentiment
        })
    
    # Pass all analyzed posts to the template
    return render_template('index.html', posts=analyzed_posts)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
