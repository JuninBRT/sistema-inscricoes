import os
from datetime import datetime


API_URL = os.getenv("INSCRICOES_API_URL", "http://localhost:8000").rstrip("/")
ANO_ATUAL = datetime.now().year


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
HUB_EQUIPAMENTOS_OPCOES = [
    "Sim, a minha organização ou projeto é atendido pelo Banco de Alimentos.",
    "Sim, a minha organização ou projeto é atendido pelo Cozinha Solidária.",
    "Sim, a minha organização ou projeto já realizou atividades nas Hortas da Ação da Cidadania.",
    "Não, nunca fui atendido por nenhum equipamento do Hub. Esta é a primeira vez.",
]
HUB_EQUIPAMENTOS_ATENDIDOS = HUB_EQUIPAMENTOS_OPCOES[:3]
ACEITE_DADOS = "Li e Aceito"
IMAGEM_EXTENSOES_PERMITIDAS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}

FIELD_CONTROL_STYLE = {
    "width": "100%",
    "background": "white",
    "border": "0",
    "border_bottom": "1px solid #9ca3af",
    "border_radius": "0",
}
SELECT_STYLE = {
    **FIELD_CONTROL_STYLE,
    "min_height": "40px",
    "padding": "0 0.75rem",
}

FORM_RED = "var(--red-9)"
LOGO_ACAO_URL = (
    "https://storage.googleapis.com/publico-acaodacidadania-org-br/media/"
    "assinatura-email/Logo-Acao-Assinatura.png"
)
