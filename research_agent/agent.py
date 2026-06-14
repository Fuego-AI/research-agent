"""Agente de pesquisa profunda (Deep Research) com Pydantic AI e OpenRouter."""

from __future__ import annotations

from typing import Any
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from openai import AsyncOpenAI

from config import (
    get_openrouter_api_key,
    get_openrouter_model_id,
    get_openrouter_base_url,
)
from tools import search_duckduckgo as _search_duckduckgo, deep_search as _deep_search, scrape_url as _scrape_url

SYSTEM_INSTRUCTIONS = """
Você é um Agente de Pesquisa Profunda (Deep Research Agent) de elite, e com conhecimento em diversas áreas do conhecimento humano, buscando auxiliar o usuário em sua pesquisa e em insights filosóficos que possam ser aplicados na vida real, a partir dos temas que os usuários estão buscando.

### Princípios de Operação:
1. **Dados em Tempo Real:** Se a pergunta exige dados atuais ou fatos que você não conhece com 100% de certeza, use as ferramentas de busca disponíveis imediatamente.
2. **Citações Obrigatórias:** Cite títulos e URLs de todas as fontes utilizadas na sua resposta final.
3. **Análise Profunda:** Para temas complexos, realize múltiplas buscas para cobrir diferentes ângulos antes de sintetizar a resposta.
4. **Honestidade:** Se a informação for inconclusiva após a pesquisa, informe ao usuário.
5. **Precisão:** Se a informação for precisa, informe ao usuário.
6. **Estrutura de envio:** Estruture um relatório claro e organizado em formato de markdown para o usuário com a seguinte estrutura:
     
  - Sumário geral do relatório
  - Propósito executivo de aplicação prática de como o conhecimento do relatório pode ser aplicado na vida real, quando este for relacionado sobre algum assunto específico objeto de pesquisa, que não seja um assunto genérico ou com meros fins financeiros e lucrativos
  - Lista com títulos de cada seção do relatório
  - Seções detelhadas de citações e fontes utilizadas para a elaboração do relatório
  - Sugestão de assuntos relacionados para aprofundamento do conhecimento
""".strip()


def create_openrouter_model() -> OpenAIChatModel:
    """Configura o modelo via OpenRouter usando um cliente OpenAI customizado através de um Provider."""
    client = AsyncOpenAI(
        base_url=get_openrouter_base_url(),
        api_key=get_openrouter_api_key(),
        default_headers={
            "HTTP-Referer": "https://github.com/pydantic/pydantic-ai",
            "X-Title": "Deep Research Agent",
        }
    )
    return OpenAIChatModel(
        get_openrouter_model_id(),
        provider=OpenAIProvider(openai_client=client)
    )


research_agent = Agent(
    create_openrouter_model(),
    instructions=SYSTEM_INSTRUCTIONS,
    retries=2,
)


@research_agent.tool
async def search_duckduckgo(ctx: RunContext[Any], query: str) -> list[dict[str, Any]]:
    """
    Realiza uma busca no DuckDuckGo para encontrar informações atualizadas.
    Use isto para obter fatos, notícias ou referências rápidas.
    """
    return _search_duckduckgo(query)


@research_agent.tool
async def deep_search(ctx: RunContext[Any], queries: list[str]) -> list[dict[str, Any]]:
    """
    Realiza buscas profundas e paralelas para múltiplos termos ou ângulos de um assunto.
    Ideal para pesquisas complexas, temas acadêmicos ou técnicos.
    """
    return _deep_search(queries)

@research_agent.tool
async def scrape_url(ctx: RunContext[Any], url: str) -> str:
    """
    Realiza a raspagem de um URL para obter informações atualizadas.
    Use isto para obter informações de sites específicos.
    """
    return _scrape_url(url)


@research_agent.tool
async def ler_arquivo(ctx: RunContext[Any], nome_arquivo: str) -> str:
    """
    Lê o conteúdo de um arquivo local do projeto.
    Use quando o usuário pedir para analisar um documento específico.
    """
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
    return conteudo

@research_agent.tool
async def ler_biblioteca(ctx: RunContext[Any], nome_arquivo: str) -> str:
    """
    Lê arquivos da biblioteca local do projeto: livros, artigos científicos e documentos de referência.
    Use isto quando o usuário pedir análise de um material acadêmico ou quando o contexto
    da pesquisa se beneficiar de referências locais já catalogadas.
    Para saber quais arquivos estão disponíveis, use primeiro a tool listar_arquivos.
    """
    with open(f"biblioteca/{nome_arquivo}", "r", encoding="utf-8") as f:
        return f.read()

@research_agent.tool
async def listar_arquivos(ctx: RunContext[Any]) -> list[str]:
    """
    Lista todos os arquivos disponíveis na biblioteca local do projeto. É pré-requisito obrigatório para utilizar a tool ler_biblioteca.
    Use isto para encontrar arquivos que tenham correlação com o tema da pesquisa do usuário dentro da sua base de dados
    Estão disponíveis livros, artigos científicos, documentos, referências e obras de filosofia
    """

    import os
    arquivos = os.listdir("biblioteca")
    return arquivos