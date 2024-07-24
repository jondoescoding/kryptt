import flet as ft
from app import agent_executor

def main(page: ft.Page):
    page.title = "AI Chat Assistant"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    chat = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)

    new_message = ft.TextField(
        hint_text="Ask me anything...",
        border_radius=30,
        expand=True,
        min_lines=1,
        max_lines=5,
        multiline=True,
    )

    def send_message(e):
        if new_message.value:
            user_message = new_message.value
            chat.controls.append(ft.Text(f"You: {user_message}", selectable=True))
            new_message.value = ""
            page.update()

            # Call the agent_executor
            #response = agent_executor.stream({"input": user_message})
            
            ai_response = [print(chunk) for chunk in agent_executor.stream({"input": user_message})]
            
            chat.controls.append(ft.Text(f"AI: {ai_response}", selectable=True))
            page.update()

    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        on_click=send_message,
        icon_color=ft.colors.BLUE_400,
    )

    page.add(
        ft.Container(
            content=chat,
            expand=True,
        ),
        ft.Container(
            content=ft.Row(
                [new_message, send_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
        )
    )

ft.app(target=main)