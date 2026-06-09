import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from .constants import API_URL


def enviar_json(caminho: str, dados: dict) -> dict:
    requisicao = Request(
        f"{API_URL}{caminho}",
        data=json.dumps(dados).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(requisicao, timeout=10) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def detalhe_erro_http(erro: HTTPError) -> str:
    try:
        corpo = json.loads(erro.read().decode("utf-8"))
        detalhe = corpo.get("detail", "Erro ao comunicar com a API")
        if isinstance(detalhe, list):
            return "Revise os campos obrigatórios do formulário."
        return str(detalhe)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "Erro ao comunicar com a API"
