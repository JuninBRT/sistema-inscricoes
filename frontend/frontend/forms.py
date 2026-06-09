from .formacao_form import FORMACAO_SECTIONS
from .gastronomia_form import GASTRONOMIA_SECTIONS


def configuracao_formulario(formulario: str) -> tuple:
    if formulario == "formacao":
        return (
            FORMACAO_SECTIONS, "Formação", "nome_documento", "cpf",
            "endereco_email", "celular_whatsapp", "curso", True,
        )
    return (
        GASTRONOMIA_SECTIONS, "Escola de Gastronomia Social", "nome_civil", "cpf",
        "endereco_email", "celular", "primeira_opcao_curso", False,
    )
