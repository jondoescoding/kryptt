import flet as ft
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from loguru import logger
from dotenv import load_dotenv
import os
from retrieval import generate_response

# Load environment variables and set up MongoDB connection
load_dotenv()
ATLAS_USERNAME = os.getenv("ATLAS_USERNAME")
ATLAS_PASSWORD = os.getenv("ATLAS_PASSWORD")
URI = f"mongodb+srv://{ATLAS_USERNAME}:{ATLAS_PASSWORD}@serverlessinstance1.2pjfhb1.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance1"

logger.add('app.log', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

def load_articles_from_db():
    articles = []
    try:
        client = MongoClient(URI, server_api=ServerApi('1'))
        db = client['crypt']
        collections = ["rekt_news", "crypto_news", "newscatcher_news", "youtube_news"]
        
        for collection in collections:
            cursor = db[collection].find({})
            for doc in cursor:
                articles.append({
                    'title': doc.get('title', 'No title'),
                    'banner': doc.get('media_thumbnail', ''),
                    'url': doc.get('link', 'No link'),
                    'published': doc.get('published', '')
                })
        
        client.close()
        logger.info(f"Loaded {len(articles)} articles from the database")
    except Exception as e:
        logger.error(f"Error loading articles from database: {e}")
    
    return sorted(articles, key=lambda x: x['published'], reverse=True)

class NewsFeed(ft.UserControl):
    def __init__(self, articles):
        super().__init__()
        self.articles = articles

    def build(self):
        self.timeline = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        for article in self.articles:
            self.timeline.controls.append(self.create_article_card(article))
        return self.timeline

    def create_article_card(self, article):
        def copy_to_clipboard(e, url):
            self.page.set_clipboard(url)
            self.page.open(ft.SnackBar(ft.Text("Link copied to clipboard!")))

        try:
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Image(
                            src=article['banner'],
                            width=300,
                            height=200,
                            fit=ft.ImageFit.COVER
                        ),
                        ft.Text(article['title'], size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            article['url'], 
                            size=12, 
                            color=ft.colors.BLUE,
                        ),
                        ft.ElevatedButton(
                            "Copy Link",
                            on_click=lambda e: copy_to_clipboard(e, article['url'])
                        )
                    ]),
                    padding=10
                ),
                width=350  # Ensure the card fits the total size of the photo
            )
        except Exception as e:
            logger.error(f"Error creating article card: {e}")
            return ft.Text("Error displaying article")

class ChatInterface(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        self.new_message = ft.TextField(hint_text="Type your message here...", expand=True)
        self.send_button = ft.IconButton(icon=ft.icons.SEND)
        self.loading_indicator = ft.ProgressRing(visible=False)

    def build(self):
        return ft.Column([
            ft.Text("Kryptt AI Chat", size=32, weight=ft.FontWeight.BOLD),
            self.chat,
            ft.Row([self.new_message, self.send_button, self.loading_indicator])
        ])

    def add_message(self, sender: str, message: str):
        emoji = "🤖" if sender == "Kryptt" else "👤"
        self.chat.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"{emoji} {sender}", weight=ft.FontWeight.BOLD),
                    ft.Text(message)
                ]),
                bgcolor=ft.colors.BLUE_GREY_900 if sender == "You" else ft.colors.BLUE_GREY_700,
                border_radius=8,
                padding=10,
                margin=ft.margin.only(bottom=10)
            )
        )
        self.update()

    async def send_message(self, e):
        if not self.new_message.value:
            return
        
        user_message = self.new_message.value
        self.new_message.value = ""
        self.update()

        self.add_message("You", user_message)

        self.loading_indicator.visible = True
        self.update()

        ai_response = generate_response(user_message)

        self.loading_indicator.visible = False
        
        self.add_message("Kryptt", ai_response)

class NewsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/news"
        
        self.sidebar = ft.NavigationRail(
            selected_index=None,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.HOME,
                    selected_icon=ft.icons.HOME,
                    label="Home",
                ),
            ],
            on_change=self.on_sidebar_change,
        )

        articles = load_articles_from_db()
        self.news_feed = NewsFeed(articles)
        self.chat_interface = ChatInterface(self.page)

        content = ft.Row([
            ft.Container(content=self.news_feed, expand=1, margin=10),
            ft.VerticalDivider(width=1),
            ft.Container(content=self.chat_interface, expand=1, margin=10)
        ], expand=True)

        self.controls = [
            ft.Row([
                self.sidebar,
                ft.VerticalDivider(width=1),
                content
            ], expand=True)
        ]

        self.chat_interface.send_button.on_click = self.handle_send
        self.chat_interface.new_message.on_submit = self.handle_send

    def on_sidebar_change(self, e):
        if e.control.selected_index == 0:  # Home button clicked
            self.page.go("/")  # Navigate to the home page

    async def handle_send(self, e):
        await self.chat_interface.send_message(e)

    def did_mount(self):
        self.chat_interface.add_message("Kryptt", "Hello! I'm Kryptt, your cryptocurrency social monitor and trading assistant. How can I help you today?")
        self.update()