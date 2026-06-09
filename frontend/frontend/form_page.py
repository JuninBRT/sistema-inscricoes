import reflex as rx

from .layout import (
    cabecalho_formulario,
    feedback_publico,
    layout_publico,
    link_pagina_inicial,
    navegacao_etapas,
    secoes_por_etapa,
)
from .state import FormularioState


def tela_confirmacao_inscricao(titulo: str, subtitulo: str) -> rx.Component:
    return rx.card(
        cabecalho_formulario(titulo, subtitulo),
        rx.box(
            rx.box(
                rx.text(
                    "Inscrição enviada com sucesso.",
                    size="3",
                    weight="bold",
                    color="#067647",
                    align="center",
                ),
                role="status",
                border_radius="8px",
                padding="1rem",
                width="100%",
                background_color="#ecfdf3",
                border="1px solid #12b76a",
            ),
            padding="2rem 3rem 2.5rem",
            width="100%",
        ),
        width="100%",
        padding="0",
        overflow="hidden",
    )


def pagina_formulario(
    titulo: str,
    subtitulo: str,
    secoes: list,
    on_submit,
    etapa,
    on_voltar,
    on_mount,
) -> rx.Component:
    return layout_publico(
        titulo,
        subtitulo,
        rx.vstack(
            link_pagina_inicial(),
            rx.cond(
                FormularioState.inscricao_enviada,
                tela_confirmacao_inscricao(titulo, subtitulo),
                rx.card(
                    cabecalho_formulario(titulo, subtitulo),
                    rx.form.root(
                        rx.vstack(
                            *secoes_por_etapa(secoes, etapa),
                            feedback_publico(),
                            navegacao_etapas(etapa, len(secoes), on_voltar),
                            spacing="4",
                            width="100%",
                        ),
                        on_submit=on_submit,
                        no_validate=True,
                        reset_on_submit=False,
                        width="100%",
                        padding="2rem 3rem 2.5rem",
                    ),
                    width="100%",
                    padding="0",
                    overflow="hidden",
                ),
            ),
            spacing="3",
            width="100%",
            on_mount=on_mount,
        ),
        exibir_titulo=False,
    )
