import re
import unicodedata
from datetime import datetime


def slug(campo: str) -> str:
    texto = unicodedata.normalize("NFKD", campo)
    texto = texto.encode("ascii", "ignore").decode("ascii").lower()
    texto = re.sub(r"[^a-z0-9]+", "_", texto).strip("_")
    return texto or "campo"


def q(
    label: str,
    name: str | None = None,
    kind: str = "text",
    options: list[str] | None = None,
    required: bool = False,
    full: bool = False,
    placeholder: str = "",
    hint: str = "",
    visible_if: tuple[str, str | list[str]] | None = None,
    label_link: tuple[str, str] | None = None,
    subfields: list[dict] | None = None,
) -> dict:
    return {
        "label": label,
        "name": name or slug(label),
        "kind": kind,
        "options": options or [],
        "required": required,
        "full": full,
        "placeholder": placeholder,
        "hint": hint,
        "visible_if": visible_if,
        "label_link": label_link,
        "subfields": subfields or [],
    }

def form_valor(form_data: dict, chave: str) -> str:
    valor = form_data.get(chave, "")
    return "" if valor is None else str(valor).strip()


def formatar_telefone(valor: str) -> str:
    digitos = re.sub(r"\D", "", valor or "")[:11]
    if not digitos:
        return ""

    if len(digitos) <= 2:
        return f"({digitos}"

    ddd = digitos[:2]
    numero = digitos[2:]
    if len(numero) <= 5:
        return f"({ddd}) {numero}"

    return f"({ddd}) {numero[:5]}-{numero[5:]}"


def respostas_formulario(form_data: dict) -> dict:
    respostas = {chave: form_valor(form_data, chave) for chave in form_data}
    respostas["carimbo_data_hora"] = datetime.now().isoformat(timespec="seconds")
    return respostas


def campo_visivel(campo: dict, respostas: dict) -> bool:
    condicao = campo.get("visible_if")
    if condicao is None:
        return True

    chave, esperado = condicao
    valor = form_valor(respostas, chave)
    if isinstance(esperado, list):
        return valor in esperado
    return valor == esperado


def primeiro_campo_obrigatorio_faltando(
    secoes: list,
    respostas: dict,
    etapa: int | None = None,
) -> tuple[int, str] | None:
    indices = [etapa] if etapa is not None else range(len(secoes))
    for indice in indices:
        for campo in secoes[indice][1]:
            if not campo.get("required") or not campo_visivel(campo, respostas):
                continue
            for subcampo in campo.get("subfields", []):
                if not form_valor(respostas, subcampo["name"]):
                    return indice, f"{campo['label']} ({subcampo['label']})"
            if campo.get("subfields"):
                continue
            if not form_valor(respostas, campo["name"]):
                return indice, campo["label"]
    return None


def indice_campo(secoes: list, nome: str) -> int:
    for indice, secao in enumerate(secoes):
        for campo in secao[1]:
            if campo["name"] == nome:
                return indice
    return 0


def nomes_campo(campo: dict) -> list[str]:
    subcampos = campo.get("subfields", [])
    if subcampos:
        return [subcampo["name"] for subcampo in subcampos]
    return [campo["name"]]


def campos_etapa(secoes: list, etapa: int | None) -> list[dict]:
    if etapa is None or etapa < 0 or etapa >= len(secoes):
        return []
    return secoes[etapa][1]


def etapa_attr(formulario: str) -> str:
    return f"etapa_{formulario}"
