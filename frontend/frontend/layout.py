import reflex as rx

from .constants import FORM_RED, LOGO_ACAO_URL
from .field_components import secao_publica
from .state import FormularioState


def feedback_publico() -> rx.Component:
    return rx.cond(
        FormularioState.mensagem != "",
        rx.box(
            rx.text(
                FormularioState.mensagem,
                size="2",
                weight="bold",
                style={
                    "color": rx.cond(FormularioState.erro, "#b42318", "#067647"),
                },
            ),
            role="alert",
            border_radius="8px",
            padding="0.85rem",
            width="100%",
            style={
                "background_color": rx.cond(FormularioState.erro, "#fef3f2", "#ecfdf3"),
                "border": rx.cond(
                    FormularioState.erro,
                    "1px solid #f04438",
                    "1px solid #12b76a",
                ),
            },
        ),
    )


def link_pagina_inicial() -> rx.Component:
    return rx.link(
        "Página inicial",
        href="/",
        color=FORM_RED,
        text_decoration="underline",
        width="fit-content",
        _hover={"color": "var(--red-10)"},
    )


def layout_publico(
    titulo: str,
    subtitulo: str,
    conteudo: rx.Component,
    exibir_titulo: bool = True,
) -> rx.Component:
    cabecalho = []
    if exibir_titulo:
        cabecalho.append(
            rx.vstack(
                rx.heading(titulo, size="7"),
                rx.text(subtitulo, color="gray.11"),
                spacing="2",
                width="100%",
            )
        )

    return rx.box(
        rx.box(
            rx.vstack(
                *cabecalho,
                conteudo,
                spacing="6",
                width="100%",
            ),
            width="100%",
            max_width="1100px",
            margin_x="auto",
            padding_x="24px",
            padding_y="40px",
        ),
        min_height="100vh",
        background="gray.1",
    )


def secoes_por_etapa(secoes: list, etapa) -> list[rx.Component]:
    return [
        rx.cond(etapa == indice, secao_publica(*secao), rx.fragment())
        for indice, secao in enumerate(secoes)
    ]


def navegacao_etapas(etapa, total: int, on_voltar) -> rx.Component:
    return rx.vstack(
        rx.text("Etapa ", etapa + 1, f" de {total}", size="2", color="gray.11"),
        rx.hstack(
            rx.button(
                "Voltar",
                type="button",
                variant="soft",
                color_scheme="red",
                on_click=on_voltar,
                visibility=rx.cond(etapa > 0, "visible", "hidden"),
            ),
            rx.button(
                rx.cond(etapa == total - 1, "Enviar inscrição", "Avançar"),
                type="submit",
                background=FORM_RED,
                color="white",
                width="180px",
                _hover={"background": "var(--red-10)", "cursor": "pointer"},
            ),
            justify="between",
            width="100%",
            wrap="wrap",
        ),
        spacing="2",
        width="100%",
    )


def cabecalho_destaque(etiqueta: str, titulo: str, aba: str | None = None) -> rx.Component:
    aba_componentes = []
    if aba:
        aba_componentes.append(
            rx.center(
                rx.box(
                    rx.text(aba, color="white", size="5", weight="bold", align="center"),
                    background=FORM_RED,
                    border="4px solid white",
                    border_radius="8px",
                    padding_y="0.35rem",
                    padding_x="2.5rem",
                    min_width="280px",
                    box_shadow="0 2px 8px rgba(0, 0, 0, 0.16)",
                ),
                width="100%",
                margin_top="-1.4rem",
            )
        )

    return rx.vstack(
        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text(etiqueta, color="white", size="3", weight="bold"),
                    rx.heading(titulo.upper(), color="white", size="8", weight="regular"),
                    spacing="2",
                    align="start",
                    flex="1",
                ),
                rx.image(
                    src=LOGO_ACAO_URL,
                    alt="Ação da Cidadania",
                    width="130px",
                    max_width="100%",
                    style={"filter": "brightness(0) invert(1)"},
                ),
                justify="between",
                align="center",
                gap="2rem",
                wrap="wrap",
                width="100%",
            ),
            background=FORM_RED,
            padding="2.5rem 3rem",
            width="100%",
        ),
        *aba_componentes,
        spacing="0",
        width="100%",
    )


def cabecalho_formulario(titulo: str, subtitulo: str) -> rx.Component:
    return cabecalho_destaque("FORMULÁRIO DE INSCRIÇÃO", titulo, "INFORMAÇÕES")


def card_projeto(titulo: str, descricao: str, href: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.box(
                rx.heading(titulo, size="4", align="center", color="white"),
                background=FORM_RED,
                padding_y="0.6rem",
                padding_x="1rem",
                width="100%",
            ),
            rx.vstack(
                rx.text(descricao, color="gray.11"),
                rx.link(
                    rx.button("Abrir formulário", background=FORM_RED, color="white", width="100%"),
                    href=href,
                    width="100%",
                ),
                spacing="4",
                align="start",
                width="100%",
                padding="1.25rem",
            ),
            spacing="0",
            width="100%",
        ),
        width="100%",
        padding="0",
        overflow="hidden",
    )
