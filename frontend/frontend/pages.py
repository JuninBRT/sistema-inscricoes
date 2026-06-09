import reflex as rx

from .components import cabecalho_destaque, card_projeto, layout_publico, pagina_formulario
from .forms import FORMACAO_SECTIONS, GASTRONOMIA_SECTIONS
from .state import FormularioState


def index() -> rx.Component:
    return layout_publico(
        "Sistema de Inscrições",
        "Escolha o formulário do projeto desejado.",
        rx.card(
            cabecalho_destaque("SISTEMA DE INSCRIÇÕES", "Escolha o formulário"),
            rx.box(
                rx.grid(
                    card_projeto(
                        "Formação",
                        "Inscrição para cursos do projeto Formação.",
                        "/formacao",
                    ),
                    card_projeto(
                        "Escola de Gastronomia",
                        "Inscrição para a Escola de Gastronomia Social.",
                        "/gastronomia",
                    ),
                    gap="1rem",
                    width="100%",
                    grid_template_columns="repeat(auto-fit, minmax(260px, 1fr))",
                ),
                padding="2rem 3rem 2.5rem",
            ),
            width="100%",
            padding="0",
            overflow="hidden",
        ),
        exibir_titulo=False,
    )


def formacao() -> rx.Component:
    return pagina_formulario(
        "Formação",
        "Formulário de inscrição do projeto Formação.",
        FORMACAO_SECTIONS,
        FormularioState.avancar_ou_enviar_formacao,
        FormularioState.etapa_formacao,
        FormularioState.voltar_formacao,
        FormularioState.iniciar_formacao,
    )


def gastronomia() -> rx.Component:
    return pagina_formulario(
        "Escola de Gastronomia Social",
        "Formulário de inscrição da Escola de Gastronomia Social.",
        GASTRONOMIA_SECTIONS,
        FormularioState.avancar_ou_enviar_gastronomia,
        FormularioState.etapa_gastronomia,
        FormularioState.voltar_gastronomia,
        FormularioState.iniciar_gastronomia,
    )

