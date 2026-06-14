"""Ferramentas de busca e utilitários para o Deep Research Agent."""

from __future__ import annotations

from typing import Any
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup


def search_duckduckgo(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """
    Realiza uma busca no DuckDuckGo e retorna os resultados.
    
    Args:
        query: O termo de busca.
        max_results: Número máximo de resultados a retornar.
        
    Returns:
        Uma lista de dicionários contendo 'title', 'href' (url) e 'body' (snippet).
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return results
    except Exception as e:
        print(f"Erro ao buscar no DuckDuckGo: {e}")
        return []


def deep_search(queries: list[str], results_per_query: int = 3) -> list[dict[str, Any]]:
    """
    Realiza buscas paralelas (sequenciais para evitar rate limit agressivo) para múltiplos termos.
    
    Args:
        queries: Lista de termos de busca.
        results_per_query: Resultados por termo.
        
    Returns:
        Lista consolidada de resultados.
    """
    all_results = []
    for q in queries:
        results = search_duckduckgo(q, max_results=results_per_query)
        for r in results:
            r['query'] = q  # Marcar de qual busca veio
        all_results.extend(results)
    return all_results

def scrape_url(url: str) -> str:
    """
    Lê todo conteúdo da página, e realiza uma síntese sobre o que foi lido

    Args:
        url: a URL da página que será lida
        

    Returns:
            O conteúdo total da URL acessada 
    """
    
    try: 
        resposta = requests.get(url)
        soup = BeautifulSoup(resposta.text, "html.parser")
        return soup.get_text()

    except Exception as e: 
        print(f"Erro ao acessar a URL")
        return""
