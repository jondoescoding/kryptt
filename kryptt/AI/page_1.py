import flet as ft
from agent import agent_executor

class ChatView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/chat"
        
        # Create a sidebar with a home button
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

        self.chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        self.new_message = ft.TextField(hint_text="Type your message here...", expand=True)
        self.send_button = ft.IconButton(icon=ft.icons.SEND)
        self.loading_indicator = ft.ProgressRing(visible=False)
        
        chat_content = ft.Column([
            ft.Text("Kryptt AI Chat", size=32, weight=ft.FontWeight.BOLD),
            self.chat,
            ft.Row([self.new_message, self.send_button, self.loading_indicator])
        ], expand=True)

        # Use a Row to combine the sidebar and chat content
        self.controls = [
            ft.Row([
                self.sidebar,
                ft.VerticalDivider(width=1),
                chat_content
            ], expand=True)
        ]
        
        self.send_button.on_click = self.send_message
        self.new_message.on_submit = self.send_message
        self.add_message("Kryptt", "Hello! I'm Kryptt, your cryptocurrency social monitor and trading assistant. Ask me what tools I have availabe to get started.")

    def on_sidebar_change(self, e):
        if e.control.selected_index == 0:  # Home button clicked
            self.page.go("/")  # Navigate to the home page

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
        self.page.update()

    async def send_message(self, e):
        if not self.new_message.value:
            return
        
        user_message = self.new_message.value
        self.new_message.value = ""
        self.page.update()

        # Add user message to the chat
        self.add_message("You", user_message)

        # Show loading indicator
        self.loading_indicator.visible = True
        self.page.update()

        # Get AI response using agent_executor
        ai_response = await agent_executor.ainvoke({"input": user_message})
        ai_response = ai_response["output"]

        # Hide loading indicator
        self.loading_indicator.visible = False
        
        # Add AI response to the chat
        self.add_message("Kryptt", ai_response)