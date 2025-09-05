from gnews import GNews

def get_google_news():
    # Initialize the GNews object
    google_news = GNews()
    
    # Fetch the top news
    top_news = google_news.get_top_news()
    
    # Return the articles
    return top_news

def getNewsUrl():
    return 'https://news.google.com/'

# Example usage
if __name__ == "__main__":
    news_articles = get_google_news()
    if news_articles:
        for article in news_articles:
            print(f"Title: {article['title']}")
            print(f"Description: {article['description']}")
            print(f"URL: {article['url']}")
            print()
    else:
        print("Failed to retrieve news articles.")
