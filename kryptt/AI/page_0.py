import flet as ft
from page_1 import ChatView
from page_2 import NewsView

def main(page: ft.Page):
    page.title = "Kryptt AI"
    page.theme_mode = ft.ThemeMode.DARK

    def route_change(route):
        page.views.clear()
        
        def go_home(e):
            page.go("/")

        app_bar = ft.AppBar(
            leading=ft.IconButton(ft.icons.HOME, on_click=go_home),
            leading_width=40,
            title=ft.Text("Kryptt AI"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

        if page.route == "/news":
            page.views.append(NewsView(page))
        elif page.route == "/chat":
            page.views.append(ChatView(page))
        else:
            # Home screen
            page.views.append(
                ft.View(
                    "/",
                    [
                        app_bar,
                        ft.Column(
                            [
                                ft.Text("Welcome to Kryptt AI", size=32, weight=ft.FontWeight.BOLD),
                                ft.Text("Your cryptocurrency social monitor and trading assistant", size=16),
                                ft.Container(height=20),
                                ft.Text("Contact Information:", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("Twitter: @jondoescoding"),
                                ft.Text("Email: jonathan.white.jm@gmail.com"),
                                ft.Text("LinkedIn: jonathanwhite-jm"),
                                ft.Container(height=40),
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Chat", on_click=lambda _: page.go("/chat")),
                                        ft.ElevatedButton("News Feed", on_click=lambda _: page.go("/news")),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.NavigationBar(
                            destinations=[
                                ft.NavigationBarDestination(icon=ft.icons.HOME, label="Home"),
                                ft.NavigationBarDestination(icon=ft.icons.CHAT, label="Chat"),
                                ft.NavigationBarDestination(icon=ft.icons.FEED, label="News Feed"),
                            ],
                            on_change=lambda e: page.go("/news" if e.control.selected_index == 2 else "/chat" if e.control.selected_index == 1 else "/"),
                        ),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)