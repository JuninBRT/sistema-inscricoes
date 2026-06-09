import reflex as rx

from .pages import formacao, gastronomia, index


app = rx.App()
app.add_page(index, route="/")
app.add_page(formacao, route="/formacao")
app.add_page(gastronomia, route="/gastronomia")
