# 🔎 Agente de Pesquisa Profunda (Deep Research Agent) - OpenRouter Edition

Este é um assistente virtual inteligente que realiza pesquisas detalhadas na internet. Ele utiliza o **OpenRouter** para acessar os modelos de linguagem mais avançados do mercado (como Gemini, Claude ou GPT) e o **DuckDuckGo** para buscar informações em tempo real.

Diferente de um chat comum, este agente consegue "mergulhar fundo" em um assunto, pesquisando múltiplos ângulos simultaneamente e organizando tudo de forma lógica e referenciada.

---

## 🌟 O que ele faz?

-   **Pesquisa Multi-Ângulos:** Para perguntas complexas, ele realiza múltiplas buscas paralelas para cobrir todos os aspectos do tema.
-   **Busca em Tempo Real:** Acesso direto à internet via DuckDuckGo para notícias e fatos atualizados.
-   **Citações e Referências:** Identifica claramente as fontes, incluindo títulos e URLs, para garantir a confiabilidade.
-   **Foco Especializado:** Otimizado para **Tecnologia**, **Humanidades** e conteúdos **Acadêmicos/Concursos**.
-   **Postura:** Para toda tarefa que envolva uma requisição do usuário o qual o LLM não tenha sido treinado para realizar, ele irá buscar as informações através de suas ferramentas de pesquisas, utilizando-se também do **DuckDuckGo**

---

## 🛠️ Como preparar para usar (Passo a Passo)

### 1. Obtenha sua chave do OpenRouter
O projeto agora utiliza o **OpenRouter**, que permite acessar diversos modelos através de uma única API.
1. Acesse o site do [OpenRouter](https://openrouter.ai/).
2. Crie uma conta e vá em **Keys** para gerar uma nova chave de API.
3. Copie a chave gerada.

### 2. Prepare o ambiente no seu computador
1. Abra a pasta do projeto no seu terminal.
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
3. Ative o ambiente:
   - Windows: `.\.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configure o arquivo de ambiente (.env)
1. Crie ou edite o arquivo `.env` na raiz do projeto.
2. Configure as seguintes variáveis:
   ```env
   OPENROUTER_API_KEY=sua_chave_aqui
   OPENROUTER_MODEL_ID=google/gemini-2.0-flash-001
   ```
   *Nota: Você pode trocar o `OPENROUTER_MODEL_ID` por qualquer modelo suportado pelo OpenRouter (ex: `anthropic/claude-3.5-sonnet`).*

---

## 🚀 Como rodar o Agente

Com tudo configurado, execute:

```bash
python app.py
```

O sistema abrirá uma interface web. O link aparecerá no terminal (ex: `http://127.0.0.1:7861`).

---

## 📂 Estrutura do Projeto

-   `app.py`: Interface de usuário (Gradio).
-   `agent.py`: Lógica do agente e integração com OpenRouter via Pydantic AI.
-   `tools.py`: Ferramentas de busca (DuckDuckGo).
-   `config.py`: Gerenciamento de configurações e variáveis de ambiente.
-   `.env`: Suas chaves secretas e preferências de modelo.

---

## ⚠️ Avisos e Boas Práticas

-   **Segurança:** Nunca compartilhe seu arquivo `.env` ou sua chave do OpenRouter.
-   **Flexibilidade:** Você pode experimentar diferentes modelos alterando o ID no `.env` para ver qual oferece os melhores resultados de pesquisa.
-   **Verificação:** Sempre revise as fontes citadas pelo agente para garantir a precisão total das informações.
