import flet as ft
from agent import agent_executor

async def main(page: ft.Page):
    page.title = "Kryptt AI Chat"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.auto_scroll = True

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    new_message = ft.TextField(
        hint_text="Type your message here...",
        expand=True,
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND,
    )

    loading_indicator = ft.ProgressRing(visible=False)

    def add_message(sender: str, message: str):
        emoji = "🤖" if sender == "Kryptt" else "👤"
        chat.controls.append(
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
        page.update()

    async def send_message(e):
        if not new_message.value:
            return
        
        user_message = new_message.value
        new_message.value = ""
        page.update()

        # Add user message to the chat
        add_message("You", user_message)

        # Show loading indicator
        loading_indicator.visible = True
        page.update()

        # Get AI response using agent_executor
        ai_response = await agent_executor.ainvoke({"input": user_message})
        ai_response = ai_response["output"]

        # Hide loading indicator
        loading_indicator.visible = False
        
        # Add AI response to the chat
        add_message("Kryptt", ai_response)

    # Set the on_click event for the send button
    send_button.on_click = send_message
    
    # Set the on_submit event for the new_message TextField
    new_message.on_submit = send_message

    page.add(
        ft.Text("Kryptt AI Chat", size=32, weight=ft.FontWeight.BOLD),
        chat,
        ft.Row([new_message, send_button, loading_indicator])
    )

    # Initial greeting
    add_message("Kryptt", "Hello! I'm Kryptt, your cryptocurrency social monitor and trading assistant. How can I help you today?")

ft.app(target=main)