from .constants import (
    ACEITE_DADOS,
    ESCOLARIDADES,
    ETNIAS,
    GENEROS,
    PARENTESCOS_CONTATO,
    RELIGIOES,
    SIM_NAO,
    TIPOS_INSTITUICAO,
    UFS,
)
from .utils import q


FORMACAO_CURSOS_OPCOES = [
    "Canto",
    "Caracterização e Maquiagem",
    "Cenografia",
    "Circo",
    "Dança",
    "Dramaturgia",
    "Figurino e Indumentária",
    "Interpretação",
    "Produção Cultural",
]
FORMACAO_APRESENTACAO = [
    (
        "O Projeto FormAção Ação da Cidadania & Shell 2026 oferece cursos gratuitos "
        "em 9 áreas artísticas, com foco em prática, teoria e formação cidadão. "
        "Com carga horária total de 200 horas/aula, os cursos serão realizados "
        "entre abril e dezembro de 2026.\n\n"
        "Podem se inscrever pessoas a partir de 18 anos, residentes na região "
        "metropolitana do Rio de Janeiro, em situação de vulnerabilidade social. "
        "*Cada candidato pode se inscrever em apenas um curso e alunos de 2024 e "
        "2025 não podem participar dos cursos em 2026.*\n\n"
        "Os estudantes selecionados receberão uma bolsa incentivo mensal de R$450, "
        "para apoio com transporte e alimentação, condicionada à frequência mensal "
        "mínima de 70%.\n\n\n\n"
        "*As inscrições devem ser realizadas por meio deste formulário, de 9 de "
        "fevereiro a 3 de março de 2026.\n\n"
        "*O processo seletivo inclui análise do formulário e uma conversa com a "
        "banca pedagógica.\n\n\n\n"
        "O Projeto FormAção Ação da Cidadania & Shell é realizado pela Ação da "
        "Cidadania, via Lei Federal de Incentivo à Cultura e tem patrocínio master "
        "da Shell.\n\n\n\n"
        "📅 Inscrições: 09/02 a 03/03/2026\n\n"
        "✅ Divulgação do resultado: 23/03/2026\n\n"
        "📍 Início das aulas: 27/04/2026\n\n\n\n"
        "Tem alguma dúvida?\n\n"
        "Entre em contato conosco pelo e-mail "
        "edital.formacao2026@projetos.acaodacidadania.org.br\n\n\n\n"
        "Boa inscrição!"
    )
]

FORMACAO_SECTIONS = [
    (
        "Apresentação",
        [],
        FORMACAO_APRESENTACAO,
    ),
    (
        "Curso e aceite",
        [
            q("Endereço de e-mail", "endereco_email", "email", required=True),
            q(
                "Você leu o Edital do projeto? Caso não tenha lido, acesse através do link",
                "leu_edital",
                "select",
                SIM_NAO, required=True,
                label_link=("https://abrelink.me/eVI", "https://abrelink.me/eVI",),
            ),
            q("Escolha seu curso", "curso", "select", FORMACAO_CURSOS_OPCOES, required=True),
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
            q("Qual a sua Deficiência?", "qual_a_sua_deficiencia", required=True, visible_if=("possui_deficiencia", "Sim")),
            q("Data de Nascimento", "data_nascimento", "date"),
            q("Digite seu CPF - Apenas números", "cpf", required=True),
            q("Digite seu documento de Identidade - Apenas números", "identidade", required=True,),
            q("Órgão Emissor", "orgao_emissor", required=True,),
            q("UF do Órgão Emissor", "uf_orgao_emissor", "select", UFS, required=True,),
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
            q("Nome do contato de emergência", "contato_emergencia_nome"),
            q("Parentesco do contato de emergência", "contato_emergencia_parentesco", "select", PARENTESCOS_CONTATO),
            q("Telefone do contato de emergência", "contato_emergencia_telefone", "tel", hint="Exemplo: (021) 00000-0000"),
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
            q("Ao submeter o formulário de inscrição, você concorda expressamente com o tratamento dos dados no seu interesse, além de concordar com a política de privacidade e proteção de dados da Ação da Cidadania.", "consentimento_dados", "select", [ACEITE_DADOS], True, True),
        ],
    ),
]
