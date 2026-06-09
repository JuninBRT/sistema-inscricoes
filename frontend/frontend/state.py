import json
import os
from datetime import datetime
from urllib.error import HTTPError, URLError

import reflex as rx

from .api import detalhe_erro_http, enviar_json
from .constants import ACEITE_DADOS, ANO_ATUAL, API_URL, IMAGEM_EXTENSOES_PERMITIDAS
from .forms import configuracao_formulario
from .utils import (
    campo_visivel,
    campos_etapa,
    etapa_attr,
    form_valor,
    formatar_telefone,
    indice_campo,
    nomes_campo,
    primeiro_campo_obrigatorio_faltando,
    respostas_formulario,
    slug,
)


class FormularioState(rx.State):
    mensagem: str = ""
    erro: bool = False
    inscricao_enviada: bool = False
    valores: dict[str, str] = {}
    rascunhos_formularios: str = rx.LocalStorage(
        "{}",
        name="acao_inscricoes_rascunhos",
        sync=True,
    )
    formulario_atual: str = ""
    etapa_formacao: int = 0
    etapa_gastronomia: int = 0

    def limpar_feedback(self):
        self.mensagem = ""
        self.erro = False

    def rascunhos_salvos(self) -> dict:
        try:
            rascunhos = json.loads(self.rascunhos_formularios or "{}")
            return rascunhos if isinstance(rascunhos, dict) else {}
        except json.JSONDecodeError:
            return {}

    def etapa_segura(self, formulario: str, etapa: int | str | None) -> int:
        total = len(configuracao_formulario(formulario)[0])
        try:
            etapa_int = int(etapa or 0)
        except (TypeError, ValueError):
            etapa_int = 0
        return max(0, min(etapa_int, total - 1))

    def salvar_rascunho_formulario(self, formulario: str | None = None):
        formulario = formulario or self.formulario_atual
        if not formulario:
            return

        rascunhos = self.rascunhos_salvos()
        rascunhos[formulario] = {
            "valores": self.valores,
            "etapa": self.etapa_atual(formulario),
        }
        self.rascunhos_formularios = json.dumps(rascunhos, ensure_ascii=False)

    def remover_rascunho_formulario(self, formulario: str | None = None):
        formulario = formulario or self.formulario_atual
        if not formulario:
            return

        rascunhos = self.rascunhos_salvos()
        rascunhos.pop(formulario, None)
        self.rascunhos_formularios = json.dumps(rascunhos, ensure_ascii=False)

    def etapa_atual(self, formulario: str) -> int:
        return getattr(self, etapa_attr(formulario))

    def definir_etapa(self, formulario: str, etapa: int):
        setattr(self, etapa_attr(formulario), etapa)
        if self.formulario_atual == formulario:
            self.salvar_rascunho_formulario(formulario)

    def iniciar_formulario(self, formulario: str):
        self.formulario_atual = formulario
        self.inscricao_enviada = False
        rascunho = self.rascunhos_salvos().get(formulario, {})
        valores = rascunho.get("valores", {}) if isinstance(rascunho, dict) else {}
        self.valores = valores if isinstance(valores, dict) else {}
        self.definir_etapa(
            formulario,
            self.etapa_segura(
                formulario,
                rascunho.get("etapa", 0) if isinstance(rascunho, dict) else 0,
            ),
        )
        self.limpar_feedback()

    def iniciar_formacao(self):
        self.iniciar_formulario("formacao")

    def iniciar_gastronomia(self):
        self.iniciar_formulario("gastronomia")

    def atualizar_campo(self, nome: str, valor: str):
        self.valores = {**self.valores, nome: valor}
        self.salvar_rascunho_formulario()
        self.limpar_feedback()

    def atualizar_telefone(self, nome: str, valor: str):
        self.atualizar_campo(nome, formatar_telefone(valor))

    async def salvar_foto_individual(self, arquivos: list[rx.UploadFile]):
        if not arquivos:
            return

        arquivo = arquivos[0]
        nome_original = os.path.basename(arquivo.filename or "")
        nome_base, extensao = os.path.splitext(nome_original)
        extensao = extensao.lower()
        tipo_conteudo = arquivo.content_type or ""

        if extensao not in IMAGEM_EXTENSOES_PERMITIDAS or (
            tipo_conteudo and not tipo_conteudo.startswith("image/")
        ):
            self.erro = True
            self.mensagem = "Envie uma imagem nos formatos JPG, PNG, GIF, WEBP, BMP ou TIFF."
            return

        nome_seguro = slug(nome_base) or "foto_individual"
        sufixo = datetime.now().strftime("%Y%m%d%H%M%S%f")
        nome_arquivo = f"{nome_seguro}_{sufixo}{extensao}"
        caminho = rx.get_upload_dir() / nome_arquivo
        caminho.write_bytes(await arquivo.read())

        self.valores = {**self.valores, "foto_individual": nome_arquivo}
        self.salvar_rascunho_formulario()
        self.limpar_feedback()

    def salvar_respostas(
        self,
        form_data: dict,
        secoes: list | None = None,
        etapa: int | None = None,
    ) -> dict:
        respostas = {**self.valores}
        campos = campos_etapa(secoes, etapa) if secoes is not None else []
        nomes = [
            nome
            for campo in campos
            for nome in nomes_campo(campo)
        ] if campos else list(form_data)

        for nome in nomes:
            if nome in form_data:
                respostas[nome] = form_valor(form_data, nome)

        for campo in campos:
            if campo_visivel(campo, respostas):
                continue
            for nome in nomes_campo(campo):
                respostas.pop(nome, None)

        self.valores = respostas
        self.salvar_rascunho_formulario()
        return respostas

    def validar_campos_obrigatorios(
        self,
        secoes: list,
        respostas: dict,
        etapa: int | None = None,
        formulario: str | None = None,
    ) -> bool:
        faltando = primeiro_campo_obrigatorio_faltando(secoes, respostas, etapa)
        if faltando is None:
            return True

        indice, label = faltando
        if formulario:
            self.definir_etapa(formulario, indice)

        self.erro = True
        self.mensagem = f"Preencha o campo obrigatório: {label}"
        return False

    def voltar_formulario(self, formulario: str):
        self.limpar_feedback()
        etapa = self.etapa_atual(formulario)
        if etapa > 0:
            self.definir_etapa(formulario, etapa - 1)

    def voltar_formacao(self):
        self.voltar_formulario("formacao")

    def voltar_gastronomia(self):
        self.voltar_formulario("gastronomia")

    def avancar_ou_enviar_formulario(
        self,
        form_data: dict,
        formulario: str,
    ):
        secoes = configuracao_formulario(formulario)[0]
        etapa = self.etapa_atual(formulario)
        form_data = self.salvar_respostas(form_data, secoes, etapa)
        if not self.validar_campos_obrigatorios(
            secoes,
            form_data,
            etapa,
            formulario,
        ):
            return

        if etapa >= len(secoes) - 1:
            self.validar_e_enviar_formulario(form_data, formulario)
            return

        self.definir_etapa(formulario, etapa + 1)
        self.limpar_feedback()

    def avancar_ou_enviar_formacao(self, form_data: dict):
        self.avancar_ou_enviar_formulario(form_data, "formacao")

    def avancar_ou_enviar_gastronomia(self, form_data: dict):
        self.avancar_ou_enviar_formulario(form_data, "gastronomia")

    def validar_e_enviar_formulario(
        self,
        form_data: dict,
        formulario: str,
    ):
        (
            secoes, projeto, nome_chave, cpf_chave,
            email_chave, telefone_chave, curso_chave, exigir_consentimento,
        ) = configuracao_formulario(formulario)
        form_data = self.salvar_respostas(
            form_data,
            secoes,
            self.etapa_atual(formulario),
        )
        if not self.validar_campos_obrigatorios(
            secoes,
            form_data,
            formulario=formulario,
        ):
            return

        if exigir_consentimento and form_valor(form_data, "consentimento_dados") != ACEITE_DADOS:
            self.definir_etapa(formulario, indice_campo(secoes, "consentimento_dados"))
            self.erro = True
            self.mensagem = (
                'Para finalizar a inscrição, selecione "Li e Aceito" na pergunta '
                "sobre tratamento dos dados."
            )
            return

        self.enviar_inscricao(
            projeto,
            form_data,
            nome_chave,
            cpf_chave,
            email_chave,
            telefone_chave,
            curso_chave,
        )

    def tratar_erro(self, erro: Exception):
        self.erro = True
        self.inscricao_enviada = False
        if isinstance(erro, HTTPError):
            self.mensagem = detalhe_erro_http(erro)
        elif isinstance(erro, URLError):
            self.mensagem = (
                "Não foi possível acessar a API. Confira se o backend FastAPI "
                f"está rodando em {API_URL}."
            )
        else:
            self.mensagem = "Não foi possível concluir a inscrição."

    def enviar_inscricao(
        self,
        projeto: str,
        form_data: dict,
        nome_chave: str,
        cpf_chave: str,
        email_chave: str,
        telefone_chave: str,
        curso_chave: str,
    ):
        self.limpar_feedback()
        form_data = self.salvar_respostas(form_data)
        nome = form_valor(form_data, nome_chave)
        cpf = form_valor(form_data, cpf_chave)
        curso = form_valor(form_data, curso_chave)

        if not nome or not cpf or not curso:
            self.erro = True
            self.mensagem = "Preencha nome, CPF e curso antes de enviar."
            return

        dados = {
            "nome": nome,
            "cpf": cpf,
            "email": form_valor(form_data, email_chave) or None,
            "telefone": form_valor(form_data, telefone_chave) or None,
            "projeto": projeto,
            "curso": curso,
            "ano": ANO_ATUAL,
            "respostas": respostas_formulario(form_data),
        }

        try:
            enviar_json("/inscricoes/", dados)
            self.erro = False
            self.mensagem = "Inscrição enviada com sucesso."
            self.inscricao_enviada = True
            self.remover_rascunho_formulario()
        except Exception as erro:
            self.tratar_erro(erro)

    def enviar_formacao(self, form_data: dict):
        self.validar_e_enviar_formulario(form_data, "formacao")

    def enviar_gastronomia(self, form_data: dict):
        self.validar_e_enviar_formulario(form_data, "gastronomia")
