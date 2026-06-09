import reflex as rx

from .constants import FIELD_CONTROL_STYLE, FORM_RED, IMAGEM_EXTENSOES_PERMITIDAS, SELECT_STYLE
from .state import FormularioState


def campo_nativo(campo: dict) -> rx.Component:
    valor = FormularioState.valores.get(campo["name"], "")
    telefone = campo["kind"] == "tel"

    if campo["kind"] == "currency_pair":
        return rx.grid(
            *[
                rx.vstack(
                    rx.text(f"{subcampo['label']}: R$", size="1", weight="medium"),
                    rx.input(
                        name=subcampo["name"],
                        id=subcampo["name"],
                        type="text",
                        value=FormularioState.valores.get(subcampo["name"], ""),
                        placeholder="0,00",
                        on_change=lambda valor, nome=subcampo["name"]: (
                            FormularioState.atualizar_campo(nome, valor)
                        ),
                        input_mode="decimal",
                        **FIELD_CONTROL_STYLE,
                    ),
                    spacing="1",
                    align="stretch",
                    width="100%",
                )
                for subcampo in campo["subfields"]
            ],
            gap="1rem",
            width="100%",
            grid_template_columns="repeat(auto-fit, minmax(160px, 1fr))",
        )

    if campo["kind"] == "image_file":
        return rx.vstack(
            rx.upload(
                rx.vstack(
                    rx.text("Clique para selecionar uma imagem ou arraste o arquivo aqui", size="2"),
                    rx.text("JPG, PNG, GIF, WEBP, BMP ou TIFF", size="1", color="gray.11"),
                    spacing="1",
                    align="center",
                    width="100%",
                ),
                id=f"{campo['name']}_upload",
                accept={"image/*": sorted(IMAGEM_EXTENSOES_PERMITIDAS)},
                multiple=False,
                max_files=1,
                on_drop=FormularioState.salvar_foto_individual,
                width="100%",
                border="1px dashed #9ca3af",
                border_radius="8px",
                background="white",
                padding="0.9rem",
                cursor="pointer",
            ),
            rx.cond(
                valor != "",
                rx.text("Arquivo selecionado: ", valor, size="1", color="gray.11"),
                rx.text("Nenhum arquivo selecionado.", size="1", color="gray.11"),
            ),
            spacing="1",
            align="stretch",
            width="100%",
        )

    if campo["kind"] == "select":
        return rx.el.select(
            rx.el.option("Selecione", value=""),
            *[rx.el.option(opcao, value=opcao) for opcao in campo["options"]],
            name=campo["name"],
            id=campo["name"],
            required=campo["required"],
            value=valor,
            on_change=lambda valor: FormularioState.atualizar_campo(campo["name"], valor),
            style=SELECT_STYLE,
        )

    if campo["kind"] == "textarea":
        return rx.text_area(
            name=campo["name"],
            id=campo["name"],
            value=valor,
            placeholder=campo["placeholder"],
            required=campo["required"],
            on_change=lambda valor: FormularioState.atualizar_campo(campo["name"], valor),
            min_height="112px",
            **FIELD_CONTROL_STYLE,
        )

    return rx.input(
        name=campo["name"],
        id=campo["name"],
        type=campo["kind"],
        value=valor,
        placeholder=campo["placeholder"] or ("(00) 00000-0000" if telefone else ""),
        required=campo["required"],
        on_change=(
            lambda valor: FormularioState.atualizar_telefone(campo["name"], valor)
        ) if telefone else (
            lambda valor: FormularioState.atualizar_campo(campo["name"], valor)
        ),
        input_mode="numeric" if telefone else "text",
        max_length=15 if telefone else None,
        **FIELD_CONTROL_STYLE,
    )


def campo_html_for(campo: dict) -> str:
    subfields = campo.get("subfields", [])
    if subfields:
        return subfields[0]["name"]
    return campo["name"]


def rotulo_campo(campo: dict) -> rx.Component:
    rotulo = rx.text(
        campo["label"],
        as_="label",
        html_for=campo_html_for(campo),
        size="2",
        weight="medium",
    )
    label_link = campo.get("label_link")
    if not label_link:
        return rotulo

    texto, href = label_link
    return rx.hstack(
        rotulo,
        rx.link(
            texto,
            href=href,
            target="_blank",
            color=FORM_RED,
            text_decoration="underline",
        ),
        spacing="1",
        align="center",
        wrap="wrap",
    )


def condicao_visivel_rx(campo: dict):
    chave, esperado = campo["visible_if"]
    valor_atual = FormularioState.valores.get(chave, "")
    if not isinstance(esperado, list):
        return valor_atual == esperado
    if not esperado:
        return False

    condicao = valor_atual == esperado[0]
    for opcao in esperado[1:]:
        condicao = condicao | (valor_atual == opcao)
    return condicao


def campo_publico(campo: dict) -> rx.Component:
    marcador = []
    if campo["required"]:
        marcador.append(rx.text("*", as_="span", color="red", weight="bold"))

    dica = []
    if campo["hint"]:
        dica.append(rx.text(campo["hint"], size="1", color="gray.11", width="100%"))

    componente = rx.vstack(
        rx.hstack(
            rotulo_campo(campo),
            *marcador,
            align="center",
            justify="between",
            width="100%",
        ),
        *dica,
        campo_nativo(campo),
        spacing="1",
        align="stretch",
        justify="end",
        width="100%",
        height="100%",
        background="#f3f4f2",
        padding="0.55rem 0.65rem",
        grid_column="1 / -1" if campo["full"] or campo["kind"] in ["textarea", "currency_pair"] else "auto",
    )

    if campo["visible_if"] is None:
        return componente

    return rx.cond(
        condicao_visivel_rx(campo),
        componente,
        rx.fragment(),
    )


def secao_publica(
    titulo: str,
    campos: list[dict],
    descricao: list[str] | None = None,
    colunas: str = "1fr",
) -> rx.Component:
    colunas_grade = "repeat(2, minmax(0, 1fr))" if colunas != "1fr" else colunas
    textos = [
        rx.text(
            texto,
            color="gray.11",
            size="2",
            white_space="pre-line",
            style={"line_height": "1.35"},
        )
        for texto in descricao or []
    ]
    grade = []
    if campos:
        grade.append(
            rx.grid(
                *[campo_publico(campo) for campo in campos],
                gap="1rem",
                width="100%",
                align_items="stretch",
                grid_template_columns=colunas_grade,
            )
        )

    return rx.vstack(
        rx.box(
            rx.heading(titulo.upper(), size="3", align="center", color="white"),
            background=FORM_RED,
            padding_y="0.5rem",
            padding_x="1rem",
            width="100%",
        ),
        *textos,
        *grade,
        spacing="2",
        width="100%",
    )

