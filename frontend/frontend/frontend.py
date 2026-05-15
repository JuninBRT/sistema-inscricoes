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
    hint: str = "",
    visible_if: tuple[str, str] | None = None,
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
PARENTESCOS_CONTATO = [
    "Mãe", "Pai", "Madrasta", "Padrasto", "Avó", "Avô", "Tia", "Tio",
    "Irmã", "Irmão", "Filha", "Filho", "Cônjuge", "Companheira(o)",
    "Amiga(o)", "Vizinha(o)", "Outro",
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
    "border": "0",
    "border_bottom": "1px solid #9ca3af",
    "border_radius": "0",
    "background": "white",
    "padding": "0 0.75rem",
}

FORM_RED = "var(--red-9)"
LOGO_ACAO_URL = (
    "https://storage.googleapis.com/publico-acaodacidadania-org-br/media/"
    "assinatura-email/Logo-Acao-Assinatura.png"
)


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


class FormularioState(rx.State):
    mensagem: str = ""
    erro: bool = False
    valores: dict[str, str] = {}
    etapa_formacao: int = 0
    etapa_gastronomia: int = 0

    def limpar_feedback(self):
        self.mensagem = ""
        self.erro = False

    def iniciar_formacao(self):
        self.valores = {}
        self.etapa_formacao = 0
        self.limpar_feedback()

    def iniciar_gastronomia(self):
        self.valores = {}
        self.etapa_gastronomia = 0
        self.limpar_feedback()

    def atualizar_campo(self, nome: str, valor: str):
        self.valores = {**self.valores, nome: valor}
        self.limpar_feedback()

    def atualizar_telefone(self, nome: str, valor: str):
        self.atualizar_campo(nome, formatar_telefone(valor))

    def salvar_respostas(self, form_data: dict) -> dict:
        respostas = {
            **self.valores,
            **{chave: form_valor(form_data, chave) for chave in form_data},
        }
        self.valores = respostas
        return respostas

    def voltar_formacao(self):
        self.limpar_feedback()
        if self.etapa_formacao > 0:
            self.etapa_formacao -= 1

    def voltar_gastronomia(self):
        self.limpar_feedback()
        if self.etapa_gastronomia > 0:
            self.etapa_gastronomia -= 1

    def avancar_ou_enviar_formacao(self, form_data: dict):
        if self.etapa_formacao >= len(FORMACAO_SECTIONS) - 1:
            self.enviar_formacao(form_data)
            return

        self.salvar_respostas(form_data)
        self.etapa_formacao += 1
        self.limpar_feedback()

    def avancar_ou_enviar_gastronomia(self, form_data: dict):
        if self.etapa_gastronomia >= len(GASTRONOMIA_SECTIONS) - 1:
            self.enviar_gastronomia(form_data)
            return

        self.salvar_respostas(form_data)
        self.etapa_gastronomia += 1
        self.limpar_feedback()

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
        except Exception as erro:
            self.tratar_erro(erro)

    def enviar_formacao(self, form_data: dict):
        self.enviar_inscricao(
            "Formação",
            form_data,
            "nome_documento",
            "cpf",
            "endereco_email",
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


GASTRONOMIA_CURSO_POPULAR = (
    "Gastronomia Popular: Conceitos e Práticas para Negócios de Alimentação - "
    "Quartas das 10:00 as 16:00"
)
GASTRONOMIA_CURSOS_OPCOES = [GASTRONOMIA_CURSO_POPULAR]
GASTRONOMIA_REINGRESSO = [
    "Sim, desejo aplicar pela primeira vez para o processo seletivo de ingresso na Escola.",
    "Não, já concluí uma formação na Escola e gostaria de aplicar para a modalidade de reingresso.",
]
ACEITE_GASTRONOMIA = [
    (
        "Concordo expressamente e estou ciente com o tratamento dos meus dados no "
        "seu interesse, além de concordar com a política de privacidade e proteção "
        "de dados da Ação da Cidadania."
    )
]

GASTRONOMIA_APRESENTACAO = [
    (
        "Este Ato de Chamamento Público e Formulário de Inscrições tem por objeto "
        "a seleção de alunas(os) interessadas(os) em participar dos cursos "
        "profissionalizantes oferecidos gratuitamente pela Ação da Cidadania por "
        "meio da Escola de Gastronomia Social."
    ),
    (
        "Importante\n\nAntes de iniciar a sua inscrição leia o Edital para acessar "
        "as informações completas sobre os requisitos de acesso, a instituição de "
        "ensino e cursos ofertados no Ciclo Formativo em vigência.\n\n"
        "📄 Link para o Edital 01/2026: https://bit.ly/editalgastronomiasocial\n\n"
        "✍🏻 Período de Inscrições Edital 01/2026\n\n"
        "Inscrições para a seleção e ingresso no curso de média duração Formação "
        "em Cozinha Brasileira: 26/02/2026 a 15/03/2026 - Inscrições Encerradas\n\n"
        "Inscrições para a seleção e ingresso no curso de curta duração Gastronomia "
        "Popular: Conceitos e Práticas para Negócios de Alimentação: 26/02/2026 a "
        "13/04/2026\n\n"
        "📢 Início das aulas Formação em Cozinha Brasileira: 13 e 14 de abril de 2026\n\n"
        "👩🏻‍🏫 Início das aulas Gastronomia Popular: Conceitos e Práticas para Negócios "
        "de Alimentação: 06 de maio de 2026"
    ),
    (
        "Sobre a Ação da Cidadania\n\nA Ação da Cidadania é uma organização sem "
        "fins lucrativos fundada pelo Betinho, sociólogo e ativista brasileiro dos "
        "direitos humanos, com atuação há mais de 30 anos no combate à fome, "
        "miséria e desigualdades sociais no Brasil. Por meio do Hub de Segurança "
        "Alimentar e Nutricional do Rio de Janeiro, a organização promove o acesso "
        "contínuo à alimentação adequada através de quatro equipamentos de alto "
        "impacto social: A Cozinha Solidária; o Banco de Alimentos; as Hortas e "
        "Áreas Verdes Agroecológicas no entorno da Sede Nacional e a Escola de "
        "Gastronomia Social."
    ),
    (
        "A Escola de Gastronomia Social\n\nA Escola de Gastronomia Social da Ação "
        "da Cidadania é um centro de formação profissional voltado para a "
        "qualificação técnica de jovens e adultos em culturas alimentares "
        "brasileiras e práticas em cozinha regionais e territoriais.\n\n"
        "Quer fazer parte dessa história? Então vem com a gente!\n\n"
        "Tem alguma dúvida?\n\nEntre em contato conosco por meio do e-mail ou telefone!\n\n"
        "✉ escoladegastronomia@acaodacidadania.org.br\n☎ + 55 (21) 99550-3637"
    ),
]

GASTRONOMIA_CURSOS_DESCRICAO = [
    (
        "Cursos de Média Duração\n\nSão cursos de formação profissional com carga "
        "horária ampliada, voltado para a introdução à conceitos e técnicas em "
        "cultura alimentar e cozinha brasileira. Possuem carga horária teórica e "
        "prática, com conteúdos expositivos dentro de sala de aula e preparos em "
        "bancadas voltadas para o processo de ensino e aprendizagem dentro do "
        "Laboratório de Práticas Alimentares. Toda a carga horária prática é "
        "acompanhada e tutorada por profissionais de referência em cozinha brasileira."
    ),
    (
        "Formação em Cozinha Brasileira - Inscrições Encerradas\n\nO curso promove "
        "a aquisição de conceitos, técnicas e habilidades básicas em culturas "
        "alimentares e cozinhas regionais brasileiras por meio de vivências práticas "
        "e aulas teórico expositivas, integrando saberes tradicionais e técnicas "
        "contemporâneas da gastronomia, contribuindo para a inclusão produtiva de "
        "jovens e adultos que desejam ingressar na gastronomia e fortalecimento da "
        "identidade cultural no setor da alimentação.\n\n"
        "Tempo de Duração: 4 a 5 meses\nCarga Horária: 180 horas\n"
        "Frequência: 2 vezes por semana presencial com atividades extracurriculares remotas\n"
        "Modalidade: Híbrido (aulas presenciais e atividades extracurriculares remotas síncronas e assíncronas)\n"
        "Horários: Segundas e quartas das 8h às 12h; ou Terças e quintas das 13h às 17h\n"
        "Data de Início: 13/04/2026 (Segundas e Quartas das 8h às 12h) e 14/04/2026 "
        "(Terças e Quintas das 13h às 17h)"
    ),
    (
        "Curso de Curta Duração\n\nSão cursos livres rápidos e temáticos promovendo "
        "aprendizado ágil e aplicado ao cotidiano.\n\n"
        "Gastronomia Popular: Conceitos e Práticas para Negócios de Alimentação\n\n"
        "O curso aborda a gastronomia popular como patrimônio, estratégia de geração "
        "de renda e fortalecimento de empreendimentos de alimentação voltados para "
        "a valorização da cozinha brasileira. A formação integra a aquisição de "
        "conceitos e práticas de gestão de negócios e serviços; técnicas e preparos "
        "da cozinha brasileira atreladas à rotinas operacionais de serviços como "
        "empreendimentos de comida de rua, buffet, eventos, catering e bares.\n\n"
        "Tempo de Duração: 2 meses\nCarga Horária: 40h\n"
        "Frequência: 1 vez por semana presencial com atividades extracurriculares remotas\n"
        "Modalidade: Híbrido (aulas presenciais e atividades extracurriculares remotas síncronas e assíncronas)\n"
        "Horários: Quartas das 10h00 às 16h00\nData de Início: 06/05/2026"
    ),
]

GASTRONOMIA_IMPORTANTE_INSCRICAO = [
    (
        "Importante\n\nPreencha todas as informações com atenção. Após o envio "
        "aguarde o calendário de convocações para o processo seletivo. Caso você "
        "seja selecionada (o) para a próxima fase, receberá orientações por meio "
        "do WhatsApp e/ou e-mail. Por isso, fique alerta."
    )
]

GASTRONOMIA_IDENTIFICACAO_DESCRICAO = [
    (
        "Preencha os dados pessoais da pessoa que fará a candidatura para os cursos, "
        "tais como: E-mail, CPF, identidade, data de nascimento, nome da mãe, etc.\n\n"
        "Importante: Esses dados são de uso restrito da Escola de Gastronomia Social "
        "e fundamentais para o cadastro estudantil e solicitação de benefícios "
        "atrelados ao apoio à permanência do(a) aluno(a) no projeto.\n\n"
        "Certifique-se das informações antes de concluir a inscrição para que todos "
        "os números e datas estejam corretos."
    )
]


GASTRONOMIA_SECTIONS = [
    (
        "Apresentação",
        [],
        GASTRONOMIA_APRESENTACAO,
    ),
    (
        "Cursos disponíveis",
        [],
        GASTRONOMIA_CURSOS_DESCRICAO,
    ),
    (
        "Política e modalidade",
        [
            q("Política de Proteção de Dados e Termo de Inscrição", "politica_termo_inscricao", "select", ACEITE_GASTRONOMIA, True),
            q("Você deseja cursar pela primeira vez uma formação na Escola de Gastronomia Social?", "primeira_formacao_egs", "select", GASTRONOMIA_REINGRESSO, True),
        ],
        GASTRONOMIA_IMPORTANTE_INSCRICAO,
    ),
    (
        "Selecione as opções de curso para os quais deseja se candidatar",
        [
            q("Assinale abaixo a primeira opção de curso", "primeira_opcao_curso", "select", GASTRONOMIA_CURSOS_OPCOES, True),
            q("Caso não seja possível a primeira opção, assinale abaixo qual seria a segunda opção de curso?", "segunda_opcao_curso_2", "select", GASTRONOMIA_CURSOS_OPCOES),
            q("Qual seria a sua terceira opção de curso?", "terceira_opcao_curso_2", "select", GASTRONOMIA_CURSOS_OPCOES),
        ],
    ),
    (
        "Identificação da(o) Candidata(o)",
        [
            q("Endereço de e-mail", "endereco_email", "email", required=True),
            q("Nome Civil", "nome_civil", required=True, full=True, hint="Como consta em seus documentos como identidade e certidão de nascimento"),
            q("Nome Social", "nome_social", full=True, hint="Caso o seu nome da documentação civil tenha sido modificado, escreva abaixo o seu nome retificado."),
            q("Data de Nascimento", "data_nascimento", "date", required=True, hint="Atenção: Preencha a data de nascimento com cuidado para que não seja informado de forma incorreta (Exemplo: Dia/Mês/Ano)"),
            q("CPF", "cpf", required=True),
            q("Identidade", "identidade", required=True, hint="Informe apenas os números sem pontuação"),
            q("Órgão Emissor", "orgao_emissor", required=True),
            q("UF do Órgão Emissor", "uf_orgao_emissor", "select", UFS, required=True),
            q("DDD + Celular", "celular", "tel", required=True, hint="Exemplo: (021) 00000-0000"),
            q("CEP", "cep"),
            q("Endereço Completo", "endereco_completo", full=True),
            q("Bairro", "bairro"),
            q("Município", "municipio"),
            q("UF", "uf", "select", UFS),
            q("Nome do contato de emergência", "contato_emergencia_nome"),
            q("Parentesco do contato de emergência", "contato_emergencia_parentesco", "select", PARENTESCOS_CONTATO),
            q("Telefone do contato de emergência", "contato_emergencia_telefone", "tel", hint="Exemplo: (021) 00000-0000"),
        ],
        GASTRONOMIA_IDENTIFICACAO_DESCRICAO,
        "repeat(auto-fit, minmax(240px, 1fr))",
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
            q("Qual deficiência?", "qual_deficiencia", full=True, visible_if=("possui_deficiencia", "Sim")),
            q("Qual seu Estado Civil?", "estado_civil", "select", ESTADOS_CIVIS),
            q("Qual é a sua profissão ou função?", "profissao_funcao"),
            q("Atualmente está trabalhando?", "esta_trabalhando", "select", SIM_NAO),
            q("Qual é a sua renda familiar?", "renda_familiar", "select", RENDA_FAMILIAR),
            q("Qual a sua situação de moradia?", "situacao_moradia", "select", MORADIA),
            q("Quantas pessoas residem com você?", "pessoas_residem", "number"),
            q("Possui quantos filhos?", "filhos", "number"),
            q("Você possui CADÚnico?", "possui_cadunico", "select", SIM_NAO),
            q("Você tem acesso a benefícios ou programas sociais?", "beneficios_sociais", "select", SIM_NAO),
            q("Quais benefícios ou programas sociais?", "quais_beneficios_sociais", full=True, visible_if=("beneficios_sociais", "Sim")),
        ],
        None,
        "repeat(auto-fit, minmax(240px, 1fr))",
    ),
    (
        "Gastronomia e território",
        [
            q("Já trabalhou em cozinhas profissionais?", "trabalhou_cozinhas_profissionais", "select", SIM_NAO),
            q("Onde trabalhou em cozinhas profissionais?", "onde_trabalhou_cozinhas", full=True, visible_if=("trabalhou_cozinhas_profissionais", "Sim")),
            q("Já fez algum curso na área da alimentação ou gastronomia?", "curso_alimentacao_gastronomia", "select", SIM_NAO),
            q("Qual curso na área da alimentação ou gastronomia?", "qual_curso_alimentacao_gastronomia", full=True, visible_if=("curso_alimentacao_gastronomia", "Sim")),
            q("Possui algum Micro ou Pequeno Empreendimento Local ou de Base Comunitária no campo da alimentação?", "possui_empreendimento_alimentacao", "select", SIM_NAO, full=True),
            q("Se sim, compartilhe conosco o link ou página do seu negócio (opcional)", "link_negocio", "url", full=True, visible_if=("possui_empreendimento_alimentacao", "Sim")),
            q("Possui Cartão Nacional de Saúde (Cartão SUS)?", "cartao_sus", "select", SIM_NAO),
            q("Pertence à alguma organização ou projeto social atendido por equipamentos pertencentes ao Hub de Segurança Alimentar da Ação da Cidadania?", "organizacao_projeto_social_hub", "select", SIM_NAO, full=True),
            q("Qual organização ou projeto social?", "qual_organizacao_projeto_social", full=True, visible_if=("organizacao_projeto_social_hub", "Sim")),
            q("Reside em alguma comunidade ou território no entorno do local onde o curso será executado?", "reside_comunidade_entorno", "select", SIM_NAO, full=True),
            q("Qual comunidade ou território?", "qual_comunidade_entorno", full=True, visible_if=("reside_comunidade_entorno", "Sim")),
        ],
        None,
        "repeat(auto-fit, minmax(260px, 1fr))",
    ),
    (
        "Saúde e acessibilidade",
        [
            q("Você tem alguma restrição alimentar?", "possui_restricao_alimentar", "select", SIM_NAO),
            q("Qual restrição alimentar?", "restricao_alimentar", full=True, visible_if=("possui_restricao_alimentar", "Sim")),
            q("Você faz algum acompanhamento médico?", "acompanhamento_medico", "select", SIM_NAO),
            q("Qual acompanhamento médico?", "qual_acompanhamento_medico", full=True, visible_if=("acompanhamento_medico", "Sim")),
            q("Você faz uso de algum medicamento?", "uso_medicamento", "select", SIM_NAO),
            q("Qual medicamento?", "qual_medicamento", full=True, visible_if=("uso_medicamento", "Sim")),
            q("Você tem plano de saúde?", "plano_saude", "select", SIM_NAO),
            q("Qual plano de saúde?", "qual_plano_saude", full=True, visible_if=("plano_saude", "Sim")),
            q("Você tem alguma alergia?", "possui_alergia", "select", SIM_NAO),
            q("Qual alergia?", "alergia", full=True, visible_if=("possui_alergia", "Sim")),
            q("Necessita de medidas de acessibilidade?", "necessita_medidas_acessibilidade", "select", SIM_NAO),
            q("Medidas de Acessibilidade - Assinale abaixo e compartilhe conosco caso necessite de um(a) mediador(a)", "medidas_acessibilidade", "textarea", full=True, visible_if=("necessita_medidas_acessibilidade", "Sim")),
        ],
        None,
        "repeat(auto-fit, minmax(240px, 1fr))",
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
            
        ],
    ),
    (
        "Histórico na Escola de Gastronomia",
        [
            q("Carregue aqui a sua foto individual", "foto_individual", "url", placeholder="Link da foto individual"),
            q("Qual(is) formações você já cursou na Escola de Gastronomia Social?", "formacoes_ja_cursadas", "textarea", full=True, visible_if=("primeira_formacao_egs", GASTRONOMIA_REINGRESSO[1])),
            q("Assinale abaixo o(s) ano(s) no qual você realizou anteriormente formações na Escola", "anos_formacoes_anteriores", full=True, visible_if=("primeira_formacao_egs", GASTRONOMIA_REINGRESSO[1])),
            
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
            q("Nome Social", "nome_social", required=True, visible_if=("possui_nome_social", "Sim")),
            q("Possui nome Artístico?", "possui_nome_artistico", "select", SIM_NAO),
            q("Nome Artístico", "nome_artistico", required=True, visible_if=("possui_nome_artistico", "Sim")),
            q("Possui algum tipo de deficiência?", "possui_deficiencia", "select", SIM_NAO),
            q("Pessoa com Deficiência", "pessoa_com_deficiencia", required=True, visible_if=("possui_deficiencia", "Sim")),
            q("Data de Nascimento", "data_nascimento", "date"),
            q("Digite seu CPF - Apenas números", "cpf", required=True),
            q("Digite seu documento de Identidade - Apenas números", "identidade"),
            q("Órgão Emissor", "orgao_emissor"),
            q("UF do Órgão Emissor", "uf_orgao_emissor", "select", UFS),
            q("Número de celular com DDD / WhatsApp", "celular_whatsapp", "tel"),
        ],
    ),
    (
        "Narrativa e contato",
        [
            q("Nos conte um pouquinho quem é você", "quem_e_voce", "textarea", full=True),
            q("Por que deseja fazer esse curso?", "motivo_curso", "textarea", full=True),
            q("Já realizou alguma formação na área cultural?", "formacao_area_cultural", "select", SIM_NAO),
            q("Qual formação na área cultural você realizou?", "qual_formacao_area_cultural", visible_if=("formacao_area_cultural", "Sim")),
            q("Você trabalha na área cultural?", "trabalha_area_cultural_opcao", "select", SIM_NAO),
            q("Se sim, como trabalha na área cultural?", "trabalha_area_cultural", "textarea", full=True, visible_if=("trabalha_area_cultural_opcao", "Sim")),
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
    valor = FormularioState.valores.get(campo["name"], "")
    telefone = campo["kind"] == "tel"

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
            width="100%",
            min_height="112px",
            background="white",
            border="0",
            border_bottom="1px solid #9ca3af",
            border_radius="0",
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
        width="100%",
        background="white",
        border="0",
        border_bottom="1px solid #9ca3af",
        border_radius="0",
    )


def campo_publico(campo: dict) -> rx.Component:
    marcador = []
    if campo["required"]:
        marcador.append(rx.text("*", as_="span", color="red", weight="bold"))

    dica = []
    if campo["hint"]:
        dica.append(rx.text(campo["hint"], size="1", color="gray.11", width="100%"))

    componente = rx.vstack(
        rx.hstack(
            rx.text(campo["label"], as_="label", html_for=campo["name"], size="2", weight="medium"),
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
        grid_column="1 / -1" if campo["full"] or campo["kind"] == "textarea" else "auto",
    )

    if campo["visible_if"] is None:
        return componente

    chave, valor = campo["visible_if"]
    return rx.cond(
        FormularioState.valores.get(chave, "") == valor,
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
                nav_publica(),
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
                reset_on_submit=False,
                width="100%",
                padding="2rem 3rem 2.5rem",
            ),
            width="100%",
            padding="0",
            overflow="hidden",
            on_mount=on_mount,
        ),
        exibir_titulo=False,
    )


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


app = rx.App()
app.add_page(index, route="/")
app.add_page(formacao, route="/formacao")
app.add_page(gastronomia, route="/gastronomia")
