# GRUPO FACULDADE — Gestão de Pedal (Dados de Emergência)

Sistema completo para **gestão de emergências em eventos de ciclismo**, com backend em FastAPI e frontend em HTML/JS.

---

## Funcionalidades

- **Cadastro** de ciclistas ("bikers"), contatos de emergência e informações de saúde.
- **Edição** de todos os dados do cadastro.
- **Busca** rápida por nome.
- **Listagem** e **exportação** dos dados para CSV.

---

## Como rodar rapidamente

### Backend

1. No terminal, execute:

    ```
    cd backend
    python -m venv .venv
    # Ativação do ambiente virtual
    # Windows:
    .venv\Scripts\activate
    # Linux/macOS:
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```

2. Acesse:
    - API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
    - Documentação Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### Endpoints Principais

| Método | Endpoint                        | Descrição                                        |
|--------|---------------------------------|--------------------------------------------------|
| POST   | /bikers                        | Cria biker (contatos de emergência opcionais)     |
| PATCH  | /bikers/{id}                   | Edição parcial dos dados do biker                 |
| GET    | /bikers/busca?nome=...         | Busca por nome                                   |
| GET    | /bikers                        | Lista todos os bikers                            |
| GET    | /bikers/{id}                   | Detalhes + contatos de emergência                 |
| POST   | /bikers/{id}/contatos          | Adiciona contato de emergência                    |
| DELETE | /contatos/{id}                 | Remove um contato de emergência                   |
| GET    | /export/csv                    | Exporta dados para CSV (backend responde JSON)    |

---

### Frontend

- Basta abrir `frontend/index.html` no navegador (duplo clique).
- Certifique-se de que o backend está rodando em `http://127.0.0.1:8000`.

#### Servir via HTTP server (opcional)

```

cd frontend
python -m http.server 5500

```

Depois acesse: [http://127.0.0.1:5500](http://127.0.0.1:5500)

---

## Estrutura de Snapshots

O diretório `snapshots` armazena registros (snapshots) do seu código para interações com IA.  
Cada snapshot inclui:

- Arquivos de código selecionados
- Estrutura do projeto (se habilitada)
- O prompt/pergunta utilizada

Personalize o comportamento via `config.json`.

---