import feedparser
from utilities import generate_unique_id
from loguru import logger

logger.add('app.log', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

def get_rekt_news_articles() -> list:
    """
    Fetches and parses the RSS feed from the Rekt News website to extract news articles.
    
    Returns:
        list: A list of dictionaries, each containing details about a Rekt News article such as title, publication date, summary, link, and image URL if available.
    """
    # URL of the Rekt News RSS feed
    rekt_news = 'https://rekt.news/rss/feed.xml'
    # Parse the RSS feed using feedparser
    feed = feedparser.parse(url_file_stream_or_string=rekt_news)
    
    logger.debug("Fetching articles from rekt news...")
    # Extract relevant information from each article in the feed
    rekt_articles = [
        {
            'data_id': generate_unique_id(article.link),
            'title': article.title,  # Title of the article
            'publication_date': article.published,  # Publication date of the article
            'summary': article.summary,  # Summary of the article
            'link': article.link,  # URL link to the full article
            'image': [link['href'] for link in article.links if link.get('rel') == 'enclosure'][0] 
            if any(link.get('rel') == 'enclosure' for link in article.links) else None  # URL of the image if available
        } for article in feed.entries
    ]
    
    logger.debug("Extracted relevant information from rekt news")
    return rekt_articles


def get_crypto_news_articles() -> list:
    """
    Fetches and parses the RSS feed from the Crypto News website to extract news articles.
    
    Returns:
        list: A list of dictionaries, each containing details about a Crypto News article such as title, link, author, publication date, tags, id, summary, and media thumbnail URL if available.
    """
    # Parse the RSS feed from Crypto News using feedparser
    feed = feedparser.parse(url_file_stream_or_string='https://crypto.news/feed/')
    
    logger.debug("Fetching articles from crypto.news")
    # Extract relevant information from each article in the feed
    article_data = [
        {
            'data_id': generate_unique_id(article.link),  # Unique ID of the article
            'title': article.title,  # Title of the article
            'link': article.link,  # URL link to the full article
            'author_detail': article.author_detail,  # Author details of the article
            'published': article.published,  # Publication date of the article
            'tags': [tag['term'] for tag in article.tags],  # Tags associated with the article
            'summary': article.summary,  # Summary of the article
            'media_thumbnail': article.media_thumbnail[0]['url'] if 'media_thumbnail' in article else None  # URL of the media thumbnail if available
        } for article in feed.entries
    ]
    
    logger.debug("Extracted relevant information from crypto news")
    return article_data