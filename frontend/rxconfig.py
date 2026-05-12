import reflex as rx

config = rx.Config(
    app_name="frontend",
    backend_port=8002,
    plugins=[
        rx.plugins.RadixThemesPlugin(),
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
