from .constants import (
    ESCOLARIDADES,
    ESTADOS_CIVIS,
    ETNIAS,
    GENEROS,
    HUB_EQUIPAMENTOS_ATENDIDOS,
    HUB_EQUIPAMENTOS_OPCOES,
    MORADIA,
    ORIENTACOES,
    PARENTESCOS_CONTATO,
    RELIGIOES,
    RENDA_FAMILIAR,
    SIM_NAO,
    UFS,
)
from .utils import q


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

GASTRONOMIA_DADOS_SOCIODEMOGRAFICOS_DESCRICAO = [
    (
        "Nesta seção você compartilhará conosco informações pessoais que nos ajudarão "
        "a compreender melhor o perfil das pessoas interessadas nos cursos da Escola "
        "de Gastronomia Social da Ação da Cidadania.\n\n"
        "Esses dados são importantes para que possamos aprimorar as nossas ações "
        "formativas, fortalecer a inclusão e garantir que nossas oportunidades "
        "cheguem a diferentes públicos.\n\n"
        "Importante: As informações serão utilizadas apenas para fins institucionais "
        "com total sigilo e respeito à privacidade dos (as) participantes."
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
        "Dados sociodemográficos",
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
        GASTRONOMIA_DADOS_SOCIODEMOGRAFICOS_DESCRICAO,
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
            q("Pertence à alguma organização ou projeto social atendido por equipamentos pertencentes ao Hub de Segurança Alimentar da Ação da Cidadania?", "organizacao_projeto_social_hub", "select", HUB_EQUIPAMENTOS_OPCOES, full=True),
            q("Qual organização ou projeto social?", "qual_organizacao_projeto_social", full=True, visible_if=("organizacao_projeto_social_hub", HUB_EQUIPAMENTOS_ATENDIDOS)),
            q("Escreva sobre a sua trajetória ou experiência em cozinha (formal ou informal) com as suas palavras", "trajetoria_cozinha", "textarea", full=True, visible_if=("organizacao_projeto_social_hub", HUB_EQUIPAMENTOS_ATENDIDOS)),
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
            q(
                "Qual é o seu custo diário com deslocamento e passagem considerando o trajeto local de origem e como destino a Escola de Gastronomia Social (Rua da Gamboa, 246, Santo Cristo - Rio de Janeiro)?",
                "custo_diario_deslocamento",
                "currency_pair",
                full=True,
                subfields=[
                    {"label": "Ida", "name": "custo_diario_deslocamento_ida"},
                    {"label": "Volta", "name": "custo_diario_deslocamento_volta"},
                ],
            ),
            q("Qual é a empresa concessionária utilizada para deslocamento no trajeto acima sinalizado?", "concessionaria_deslocamento"),

        ],
    ),
    (
        "Histórico na Escola de Gastronomia",
        [
            q("Carregue aqui a sua foto individual", "foto_individual", "image_file", full=True),
            q("Qual(is) formações você já cursou na Escola de Gastronomia Social?", "formacoes_ja_cursadas", "textarea", full=True, visible_if=("primeira_formacao_egs", GASTRONOMIA_REINGRESSO[1])),
            q("Assinale abaixo o(s) ano(s) no qual você realizou anteriormente formações na Escola", "anos_formacoes_anteriores", full=True, visible_if=("primeira_formacao_egs", GASTRONOMIA_REINGRESSO[1])),

        ],
    ),
]
