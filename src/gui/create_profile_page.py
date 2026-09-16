import flet as ft
import asyncio
from flet import TextField, MainAxisAlignment

async def main(page: ft.Page):
    password_field = TextField(value= "", hint_text = "Enter Master Password", text_align=ft.TextAlign.CENTER)

    #   Передаём данные об окне
    page.title = "Password Manager"
    page.theme_mode = "dark"
    page.window.width = 500
    page.window.height = 600
    page.window.resizable = False
    page.update()
    await page.window.center()
    
    # Отображаем окно
    page.window.visible = True
    page.update()

    #   Центрируем содержимое страницы
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    #   Получаем введёный мастер пароль
    def enter_master_password():
        master_password = password_field.value
        page.update()
        print(master_password)
        return

    #   Отладка расположение элементов (Нажатием Shift + S) потом нужно убрать
    def on_keyboard(e: ft.KeyboardEvent):
        if e.shift and e.key == "S":
            page.show_semantics_debugger = not page.show_semantics_debugger
            page.update()
    page.on_keyboard_event = on_keyboard
    
    #   Добавление элментов на страницу
    page.add(
        ft.Text(
                "Password Manager",
                weight=ft.FontWeight.W_600,
                theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                ),
        ft.Container(
            width=350,
            bgcolor=ft.Colors.BLACK,
            border_radius=ft.BorderRadius.all(20),
            padding=20,
            content=ft.Column(
                controls= [
                    ft.Row([ft.Text("Create Master Password", size=15, weight=ft.FontWeight.W_600),], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([password_field], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Button(content = "Create", on_click= enter_master_password)], alignment=ft.MainAxisAlignment.CENTER)
                    ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.FLET_APP_HIDDEN)