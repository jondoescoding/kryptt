# Imports 
import os
from datetime import datetime, timedelta
from pprint import pprint
from dotenv import load_dotenv
from pyyoutube import Client
from newscatcherapi_client import Newscatcher, ApiException
from utilities import generate_unique_id
from loguru import logger

# Environmental Variables
load_dotenv('.env')

COUNTRIES = "AD, AE, AF, AG, AI, AL, AM, AO, AQ, AR, AS, AT, AU, AW, AX, AZ, BA, BB, BD, BE, BF, BG, BH, BI, BJ, BL, BM, BN, BO, BQ, BR, BS, BT, BV, BW, BY, BZ, CA, CC, CD, CF, CG, CH, CI, CK, CL, CM, CN, CO, CR, CU, CV, CW, CX, CY, CZ, DE, DJ, DK, DM, DO, DZ, EC, EE, EG, EH, ER, ES, ET, FI, FJ, FK, FM, FO, FR, GA, GB, GD, GE, GF, GG, GH, GI, GL, GM, GN, GP, GQ, GR, GS, GT, GU, GW, GY, HK"

LANG = "af,ar,bg,bn,ca,cs,cy,cn,da,de,el,en,es,et,fa,fi,fr,gu,he,hi,hr,hu,id,it,ja,kn,ko,lt,lv,mk,ml,mr,ne,nl,no,pa,pl,pt,ro,ru,sk,sl,so,sq,sv,sw,ta,te,th,tl,tr,tw,uk,ur,vi"

def get_news_from_newscatcher() -> list:
    """
    Retrieves news articles from the Newscatcher API.
    Returns a list of news articles.
    Raises ApiException if the API request fails.
    """
    
    logger.debug("Setting up Newscatcher API client")   
    # Newscatcher API
    newscatcher = Newscatcher(api_key=os.getenv('NEWS_API'))
    
    try:
        response = newscatcher.search.get(q="DeFi, Cryptocurrency, NFTs",
            search_in="content, summary, title",
            lang=LANG,
            sort_by="date", # most recent articles are grabbed first
            page=1,
            countries=COUNTRIES,
            from_= (datetime.now() - timedelta(days=30)).strftime('%Y/%m/%d'), # changed the timeframe to 30 days from 182 days
            is_paid_content= False,
        )
        
        logger.debug("Received response from Newscatcher API")
        
        if response.status == "ok":
            logger.debug("Response status is ok, processing articles")
            newscatcher_articles = [
                {
                    "data_id": generate_unique_id(article['link']),
                    "title": article['title'],
                    "author": article['author'],
                    "authors": article['authors'],
                    "journalists": article['journalists'],
                    "published_date": article['published_date'],
                    "published_date_precision": article['published_date_precision'],
                    "updated_date": article['updated_date'],
                    "updated_date_precision": article['updated_date_precision'],
                    "link": article['link'],
                    "domain_url": article['domain_url'],
                    "full_domain_url": article['full_domain_url'],
                    "name_source": article['name_source'],
                    "is_headline": article['is_headline'],
                    "paid_content": article['paid_content'],
                    "parent_url": article['parent_url'],
                    "country": article['country'],
                    "rights": article['rights'],
                    "rank": article['rank'],
                    "media": article['media'],
                    "language": article['language'],
                    "description": article['description'],
                    "content": article['content'],
                    "word_count": article['word_count'],
                    "is_opinion": article['is_opinion'],
                    "twitter_account": article['twitter_account'],
                    "all_links": article['all_links'],
                    "all_domain_links": article['all_domain_links'],
                    "score": article['score']
                } for article in response.articles
            ]
            logger.debug("Processed articles, returning the list")
            return newscatcher_articles
    except ApiException as e:
        logger.error(f"Error: {e}")
        if e.status in [422, 403]:
            pprint(e.body)
    
    logger.debug("Returning empty list due to API error")
    return []


def extract_youtube_videos() -> list:
    """
    Extracts YouTube videos related to crypto news.
    
    Returns:
    list: A list of dictionaries containing video information.
    """
    logger.debug("Entering extract_youtube_videos function")
    
    try:
        logger.debug("Creating YouTube API client")
        client = Client(api_key=os.getenv('YOUTUBE_API_KEY'))
        
        logger.debug("Searching for YouTube videos with 'crypto news' query")
        search_results = client.search.list(
            q="crypto news",
            part='snippet',
            maxResults=50,
            order="date",
            relevance_language="en",
            type="video",
            video_caption="closedCaption",
            published_after=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z',
        )
        
        logger.debug("Processing search results")
        video_list = [
            {
                "channel_id": video.snippet.channelId,
                "channel_title": video.snippet.channelTitle,
                "data_id": generate_unique_id(f"https://www.youtube.com/watch?v={video.id.videoId}"),
                "video_url": f"https://www.youtube.com/watch?v={video.id.videoId}",
                "title": video.snippet.title,
                "description": video.snippet.description,
                "published_date": video.snippet.publishedAt,
                "thumbnail": video.snippet.thumbnails.default.url
            } for video in search_results.items
        ]
        
        logger.debug("Returning video list")
        return video_list
    except Exception as e:
        logger.error(f"Error: {e}")
    logger.debug("Returning empty list due to error")
    return []

# Example usage
youtube_link = extract_youtube_videos()
logger.info(youtube_link)