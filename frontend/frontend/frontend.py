import json
import os
import re
import unicodedata
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import reflex as rx


API_URL = os.getenv("INSCRICOES_API_URL", "http://localhost:8000").rstrip("/")
ANO_ATUAL = datetime.now().year


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
) -> dict:
    return {
        "label": label,
        "name": name or slug(label),
        "kind": kind,
        "options": options or [],
        "required": required,
        "full": full,
        "placeholder": placeholder,
    }


SIM_NAO = ["Sim", "Não"]
UFS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO",
]
GENEROS = [
    "Mulher cis", "Homem cis", "Mulher trans", "Homem trans",
    "Pessoa não-binária", "Prefiro não informar", "Outro",
]
ORIENTACOES = [
    "Heterossexual", "Homossexual", "Bissexual", "Pansexual", "Assexual",
    "Prefiro não informar", "Outro",
]
ETNIAS = ["Branca", "Preta", "Parda", "Amarela", "Indígena", "Prefiro não informar"]
RELIGIOES = [
    "Católica", "Evangélica", "Espírita", "Umbanda", "Candomblé",
    "Sem religião", "Prefiro não informar", "Outra",
]
ESCOLARIDADES = [
    "Ensino fundamental incompleto", "Ensino fundamental completo",
    "Ensino médio incompleto", "Ensino médio completo",
    "Ensino superior incompleto", "Ensino superior completo", "Pós-graduação",
]
ESTADOS_CIVIS = [
    "Solteiro(a)", "Casado(a)", "União estável", "Separado(a)",
    "Divorciado(a)", "Viúvo(a)",
]
RENDA_FAMILIAR = [
    "Sem renda", "Até 1 salário mínimo", "De 1 a 2 salários mínimos",
    "De 2 a 3 salários mínimos", "Acima de 3 salários mínimos",
]
MORADIA = ["Própria", "Alugada", "Cedida", "Ocupação", "Situação de rua", "Outra"]
TIPOS_INSTITUICAO = ["Pública", "Privada", "Comunitária", "Outro"]
ACEITE = ["Li e aceito"]

SELECT_STYLE = {
    "width": "100%",
    "min_height": "40px",
    "border": "1px solid var(--gray-7)",
    "border_radius": "6px",
    "background": "white",
    "padding": "0 0.75rem",
}


def form_valor(form_data: dict, chave: str) -> str:
    valor = form_data.get(chave, "")
    return "" if valor is None else str(valor).strip()


def respostas_formulario(form_data: dict) -> dict:
    respostas = {chave: form_valor(form_data, chave) for chave in form_data}
    respostas["carimbo_data_hora"] = datetime.now().isoformat(timespec="seconds")
    return respostas


class FormularioState(rx.State):
    mensagem: str = ""
    erro: bool = False

    def limpar_feedback(self):
        self.mensagem = ""
        self.erro = False

    def tratar_erro(self, erro: Exception):
        self.erro = True
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
        except Exception as erro:
            self.tratar_erro(erro)

    def enviar_formacao(self, form_data: dict):
        self.enviar_inscricao(
            "Formação",
            form_data,
            "nome_documento",
            "cpf",
            "email",
            "celular_whatsapp",
            "curso",
        )

    def enviar_gastronomia(self, form_data: dict):
        self.enviar_inscricao(
            "Escola de Gastronomia Social",
            form_data,
            "nome_civil",
            "cpf",
            "endereco_email",
            "celular",
            "primeira_opcao_curso",
        )


GASTRONOMIA_SECTIONS = [
    (
        "Curso e aceite",
        [
            q("Endereço de e-mail", "endereco_email", "email", required=True),
            q("Assinale abaixo a primeira opção de curso", "primeira_opcao_curso", required=True),
            q("Caso não seja possível a primeira opção, assinale abaixo qual seria a segunda opção de curso? 2", "segunda_opcao_curso_2"),
            q("Qual seria a sua terceira opção de curso?", "terceira_opcao_curso_2"),
            q("Política de Proteção de Dados e Termo de Inscrição", "politica_termo_inscricao", "select", ACEITE, True),
        ],
    ),
    (
        "Identificação",
        [
            q("Nome Civil", "nome_civil", required=True),
            q("Nome Social", "nome_social"),
            q("CPF", "cpf", required=True),
            q("Identidade", "identidade"),
            q("Data de Nascimento", "data_nascimento", "date"),
            q("Órgão Emissor", "orgao_emissor"),
            q("UF do Órgão Emissor", "uf_orgao_emissor", "select", UFS),
        ],
    ),
    (
        "Endereço e contato",
        [
            q("CEP", "cep"),
            q("Endereço Completo", "endereco_completo"),
            q("Bairro", "bairro"),
            q("Município", "municipio"),
            q("UF", "uf", "select", UFS),
            q("DDD + Celular", "celular", "tel"),
            q("Contato em caso de emergência", "contato_emergencia"),
        ],
    ),
    (
        "Perfil social",
        [
            q("Gênero", "genero", "select", GENEROS),
            q("Orientação sexual", "orientacao_sexual", "select", ORIENTACOES),
            q("Autodeclaração Étnico-Racial", "autodeclaracao_etnico_racial", "select", ETNIAS),
            q("Assinale abaixo a sua Religião", "religiao", "select", RELIGIOES),
            q("Assinale a sua Escolaridade", "escolaridade", "select", ESCOLARIDADES),
            q("Você possui alguma deficiência?", "possui_deficiencia", "select", SIM_NAO),
            q("Qual seu Estado Civil?", "estado_civil", "select", ESTADOS_CIVIS),
            q("Qual é a sua profissão ou função?", "profissao_funcao"),
            q("Atualmente está trabalhando?", "esta_trabalhando", "select", SIM_NAO),
            q("Qual é a sua renda familiar?", "renda_familiar", "select", RENDA_FAMILIAR),
            q("Qual a sua situação de moradia?", "situacao_moradia", "select", MORADIA),
            q("Quantas pessoas residem com você?", "pessoas_residem", "number"),
            q("Possui quantos filhos?", "filhos", "number"),
            q("Você possui CADÚnico?", "possui_cadunico", "select", SIM_NAO),
            q("Você tem acesso a benefícios ou programas sociais?", "beneficios_sociais", "select", SIM_NAO),
        ],
    ),
    (
        "Gastronomia e território",
        [
            q("Já trabalhou em cozinhas profissionais?", "trabalhou_cozinhas_profissionais", "select", SIM_NAO),
            q("Se sim, compartilhe conosco o link ou página do seu negócio (opcional)", "link_negocio", "url"),
            q("Já fez algum curso na área da alimentação ou gastronomia?", "curso_alimentacao_gastronomia", "select", SIM_NAO),
            q("Possui algum Micro ou Pequeno Empreendimento Local ou de Base Comunitária no campo da alimentação?", "possui_empreendimento_alimentacao", "select", SIM_NAO),
            q("Possui Cartão Nacional de Saúde (Cartão SUS)?", "cartao_sus", "select", SIM_NAO),
            q("Pertence à alguma organização ou projeto social atendido por equipamentos pertencentes ao Hub de Segurança Alimentar da Ação da Cidadania?", "organizacao_projeto_social_hub", "select", SIM_NAO),
            q("Reside em alguma comunidade ou território no entorno do local onde o curso será executado?", "reside_comunidade_entorno", "select", SIM_NAO),
        ],
    ),
    (
        "Saúde e acessibilidade",
        [
            q("Você tem alguma restrição alimentar?", "restricao_alimentar"),
            q("Você faz algum acompanhamento médico?", "acompanhamento_medico", "select", SIM_NAO),
            q("Você faz uso de algum medicamento?", "uso_medicamento", "select", SIM_NAO),
            q("Você tem plano de saúde?", "plano_saude", "select", SIM_NAO),
            q("Você tem alguma alergia?", "alergia"),
            q("Medidas de Acessibilidade - Assinale abaixo e compartilhe conosco caso necessite de um(a) mediador(a)", "medidas_acessibilidade", "textarea", full=True),
        ],
    ),
    (
        "Trajetória e escolhas",
        [
            q("Como você se imagina daqui 2, 4 ou 5 anos?", "imagina_futuro", "textarea", full=True),
            q("Conte para nós porque deseja fazer um curso na Escola de Gastronomia Social e de que forma podemos contribuir com a sua formação profissional", "motivo_escola_gastronomia", "textarea", full=True),
            q("Cite 3 defeitos seus", "defeitos", "textarea", full=True),
            q("Caso não seja possível a primeira opção, assinale abaixo qual seria a segunda opção de curso?", "segunda_opcao_curso"),
            q("E caso não sejam possíveis a primeira e segunda opções, qual seria a sua terceira opção de curso?", "terceira_opcao_curso"),
            q("Qual é o seu custo diário com deslocamento e passagem considerando o trajeto local de origem e como destino a Escola de Gastronomia Social (Rua da Gamboa, 246, Santo Cristo - Rio de Janeiro)?", "custo_diario_deslocamento"),
            q("Qual é a empresa concessionária utilizada para deslocamento no trajeto acima sinalizado?", "concessionaria_deslocamento"),
            q("Escreva sobre a sua trajetória ou experiência em cozinha (formal ou informal) com as suas palavras", "trajetoria_cozinha", "textarea", full=True),
            q("Você deseja cursar pela primeira vez uma formação na Escola de Gastronomia Social?", "primeira_formacao_egs", "select", SIM_NAO),
            q("Política de Proteção de Dados", "politica_protecao_dados", "select", ACEITE),
        ],
    ),
    (
        "Histórico na Escola de Gastronomia",
        [
            q("Qual(is) formações você já cursou na Escola de Gastronomia Social?", "formacoes_ja_cursadas", "textarea", full=True),
            q("Carregue aqui a sua foto individual", "foto_individual", "url", placeholder="Link da foto individual"),
            q("Assinale abaixo o(s) ano(s) no qual você realizou anteriormente formações na Escola", "anos_formacoes_anteriores"),
            
        ],
    ),
]

FORMACAO_SECTIONS = [
    (
        "Curso e aceite",
        [
            q("Endereço de e-mail", "endereco_email", "email", required=True),
            q("Você leu o Edital do projeto? Caso não tenha lido, acesse através do link https://abrelink.me/XoU", "leu_edital", "select", SIM_NAO),
            q("Escolha seu curso", "curso", required=True),
        ],
    ),
    (
        "Identificação",
        [
            q("Nome como consta no documento", "nome_documento", required=True),
            q("Possui nome social?", "possui_nome_social", "select", SIM_NAO),
            q("Nome Social", "nome_social"),
            q("Possui nome Artístico?", "possui_nome_artistico", "select", SIM_NAO),
            q("Nome Artístico", "nome_artistico"),
            q("Possui algum tipo de deficiência?", "possui_deficiencia", "select", SIM_NAO),
            q("Pessoa com Deficiência", "pessoa_com_deficiencia"),
            q("Data de Nascimento", "data_nascimento", "date"),
            q("Digite seu CPF - Apenas números", "cpf", required=True),
            q("Digite seu documento de Identidade - Apenas números", "identidade"),
            q("Órgão Emissor", "orgao_emissor"),
            q("UF do Órgão Emissor", "uf_orgao_emissor", "select", UFS),
            q("Número de celular com DDD / WhatsApp", "celular_whatsapp", "tel"),
            q("E-mail", "email", "email"),
        ],
    ),
    (
        "Narrativa e contato",
        [
            q("Nos conte um pouquinho quem é você", "quem_e_voce", "textarea", full=True),
            q("Por que deseja fazer esse curso?", "motivo_curso", "textarea", full=True),
            q("Já realizou alguma formação na área cultural?", "formacao_area_cultural", "select", SIM_NAO),
            q("Você trabalha da área cultural? Se sim, como?", "trabalha_area_cultural", "textarea", full=True),
            q("Contato de Emergência (Nome e Telefone)", "contato_emergencia"),
        ],
    ),
    (
        "Endereço",
        [
            q("CEP", "cep"),
            q("Logradouro", "logradouro"),
            q("Número", "numero"),
            q("Complemento", "complemento"),
            q("Bairro", "bairro"),
            q("Município", "municipio"),
            q("UF", "uf", "select", UFS),
        ],
    ),
    (
        "Perfil social e escolar",
        [
            q("Gênero", "genero", "select", GENEROS),
            q("Cor/Etnia", "cor_etnia", "select", ETNIAS),
            q("Religião", "religiao", "select", RELIGIOES),
            q("Quantas pessoas moram com você?", "pessoas_moram", "number"),
            q("Qual a sua escolaridade?", "escolaridade", "select", ESCOLARIDADES),
            q("Nome da instituição de ensino", "instituicao_ensino"),
            q("Tipo da instituição de ensino", "tipo_instituicao_ensino", "select", TIPOS_INSTITUICAO),
            q("Foi bolsista?", "bolsista", "select", SIM_NAO),
            q("Ao submeter o formulário de inscrição, você concorda expressamente com o tratamento dos dados no seu interesse, além de concordar com a política de privacidade e proteção de dados da Ação da Cidadania.", "consentimento_dados", "select", ACEITE, True, True),
        ],
    ),
]


def campo_nativo(campo: dict) -> rx.Component:
    if campo["kind"] == "select":
        return rx.el.select(
            rx.el.option("Selecione", value=""),
            *[rx.el.option(opcao, value=opcao) for opcao in campo["options"]],
            name=campo["name"],
            id=campo["name"],
            required=campo["required"],
            default_value="",
            style=SELECT_STYLE,
        )

    if campo["kind"] == "textarea":
        return rx.text_area(
            name=campo["name"],
            id=campo["name"],
            placeholder=campo["placeholder"],
            required=campo["required"],
            width="100%",
            min_height="112px",
        )

    return rx.input(
        name=campo["name"],
        id=campo["name"],
        type=campo["kind"],
        placeholder=campo["placeholder"],
        required=campo["required"],
        width="100%",
    )


def campo_publico(campo: dict) -> rx.Component:
    marcador = []
    if campo["required"]:
        marcador.append(rx.badge("Obrigatório", color_scheme="red", variant="soft"))

    return rx.vstack(
        rx.hstack(
            rx.text(campo["label"], as_="label", html_for=campo["name"], size="2", weight="medium"),
            *marcador,
            align="center",
            justify="between",
            width="100%",
        ),
        campo_nativo(campo),
        spacing="1",
        width="100%",
        grid_column="1 / -1" if campo["full"] or campo["kind"] == "textarea" else "auto",
    )


def secao_publica(titulo: str, campos: list[dict]) -> rx.Component:
    return rx.vstack(
        rx.heading(titulo, size="4"),
        rx.grid(
            *[campo_publico(campo) for campo in campos],
            gap="1rem",
            width="100%",
            grid_template_columns="repeat(auto-fit, minmax(260px, 1fr))",
        ),
        spacing="3",
        width="100%",
    )


def feedback_publico() -> rx.Component:
    return rx.cond(
        FormularioState.mensagem != "",
        rx.box(
            rx.text(FormularioState.mensagem, weight="medium"),
            border="1px solid",
            border_color=rx.cond(FormularioState.erro, "red.7", "green.7"),
            background=rx.cond(FormularioState.erro, "red.2", "green.2"),
            color=rx.cond(FormularioState.erro, "red.12", "green.12"),
            border_radius="8px",
            padding="0.85rem",
            width="100%",
        ),
    )


def nav_publica() -> rx.Component:
    return rx.hstack(
        rx.link("Início", href="/"),
        rx.link("Formação", href="/formacao"),
        rx.link("Gastronomia", href="/gastronomia"),
        spacing="5",
        wrap="wrap",
        width="100%",
    )


def layout_publico(titulo: str, subtitulo: str, conteudo: rx.Component) -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                nav_publica(),
                rx.vstack(
                    rx.heading(titulo, size="7"),
                    rx.text(subtitulo, color="gray.11"),
                    spacing="2",
                    width="100%",
                ),
                conteudo,
                spacing="6",
                width="100%",
            ),
            max_width="960px",
            padding_y="40px",
        ),
        min_height="100vh",
        background="gray.1",
    )


def pagina_formulario(
    titulo: str,
    subtitulo: str,
    secoes: list,
    on_submit,
) -> rx.Component:
    return layout_publico(
        titulo,
        subtitulo,
        rx.card(
            rx.form.root(
                rx.vstack(
                    *[secao_publica(secao_titulo, campos) for secao_titulo, campos in secoes],
                    feedback_publico(),
                    rx.button(
                        rx.icon("send", size=16),
                        "Enviar inscrição",
                        type="submit",
                        width="100%",
                    ),
                    spacing="5",
                    width="100%",
                ),
                on_submit=on_submit,
                reset_on_submit=False,
                width="100%",
            ),
            width="100%",
        ),
    )


def index() -> rx.Component:
    return layout_publico(
        "Sistema de Inscrições",
        "Escolha o formulário do projeto desejado.",
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.heading("Formação", size="5"),
                    rx.text("Inscrição para cursos do projeto Formação.", color="gray.11"),
                    rx.link(rx.button("Abrir formulário", width="100%"), href="/formacao", width="100%"),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                width="100%",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("Escola de Gastronomia", size="5"),
                    rx.text("Inscrição para a Escola de Gastronomia Social.", color="gray.11"),
                    rx.link(rx.button("Abrir formulário", width="100%"), href="/gastronomia", width="100%"),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                width="100%",
            ),
            gap="1rem",
            width="100%",
            grid_template_columns="repeat(auto-fit, minmax(260px, 1fr))",
        ),
    )


def formacao() -> rx.Component:
    return pagina_formulario(
        "Formação",
        "Formulário de inscrição do projeto Formação.",
        FORMACAO_SECTIONS,
        FormularioState.enviar_formacao,
    )


def gastronomia() -> rx.Component:
    return pagina_formulario(
        "Escola de Gastronomia Social",
        "Formulário de inscrição da Escola de Gastronomia Social.",
        GASTRONOMIA_SECTIONS,
        FormularioState.enviar_gastronomia,
    )


app = rx.App()
app.add_page(index, route="/")
app.add_page(formacao, route="/formacao")
app.add_page(gastronomia, route="/gastronomia")
