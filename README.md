# Sistema de Inscrições

Sistema para inscrições dos projetos **Formação** e **Escola de Gastronomia Social** da Ação da Cidadania.

O projeto tem dois formulários públicos separados, mas usa uma base comum de inscritos. Os dados principais do participante ficam em `alunos`, enquanto cada inscrição fica em `inscricoes` com as respostas específicas do formulário armazenadas em JSON.

## Stack

- Backend: FastAPI, SQLAlchemy, Alembic e PostgreSQL
- Frontend: Reflex
- Banco local: PostgreSQL 16 via Docker Compose

## Estrutura

```text
backend/
  app/
    models/        Modelos SQLAlchemy
    routes/        Rotas FastAPI
    schemas/       Schemas Pydantic
  alembic/         Migrations do banco
  docker-compose.yml
  Dockerfile

frontend/
  frontend/
    frontend.py    Telas Reflex
  rxconfig.py
  requirements.txt
```

## Configuração do backend

Crie o arquivo `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/inscricoes_db
```

Suba a API e o banco:

```bash
cd backend
docker compose up --build
```

Em outro terminal, aplique as migrations:

```bash
cd backend
docker compose exec api alembic upgrade head
```

A API ficará disponível em:

```text
http://localhost:8000
http://localhost:8000/docs
```

## Configuração do frontend

Instale as dependências do Reflex:

```bash
cd frontend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Rode o frontend:

```bash
reflex run
```

Se precisar definir portas explicitamente:

```bash
reflex run --frontend-port 3000 --backend-port 8002
```

O frontend usa `http://localhost:8000` como API por padrão. Para apontar para outra URL:

```bash
INSCRICOES_API_URL=http://localhost:8000 reflex run
```

## Páginas do frontend

```text
/              Página inicial
/formacao      Formulário do projeto Formação
/gastronomia   Formulário da Escola de Gastronomia Social
```

## Endpoints principais

```text
GET  /                       Health check da API
POST /inscricoes/            Cria uma inscrição
GET  /inscricoes/            Lista inscrições
GET  /inscricoes/consulta    Consulta histórico por nome ou CPF
```

Observação: a consulta de histórico não aparece nos formulários públicos. Ela está disponível na API para uso futuro no sistema de gestão de matrículas.

## Modelo de dados

- `alunos`: cadastro único do inscrito, com CPF único.
- `inscricoes`: inscrição em um projeto, vinculada ao aluno.
- `inscricoes.respostas`: JSON com as perguntas específicas de cada formulário.

## Comandos úteis

Verificar status dos containers:

```bash
cd backend
docker compose ps
```

Rodar migrations pendentes:

```bash
cd backend
docker compose exec api alembic upgrade head
```

Ver revision atual do banco:

```bash
cd backend
docker compose exec db psql -U postgres -d inscricoes_db -c "select version_num from alembic_version;"
```

Compilar o frontend sem subir servidor:

```bash
cd frontend
reflex compile
```

## Notas de desenvolvimento

- Não versionar `.env`, `.venv`, `.web`, `.states` ou `__pycache__`.
- O campo de foto individual da Escola de Gastronomia está como URL no formulário atual. Upload real de arquivo exige uma etapa posterior de armazenamento e API multipart.
- Sempre rode `alembic upgrade head` após criar ou baixar migrations novas.
