"""Verifica se o LM Studio está rodando e lista os modelos disponíveis."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from config import get_lm_studio_api_key, get_lm_studio_base_url, get_lm_studio_model_id


def main() -> int:
    base = get_lm_studio_base_url()
    url = f"{base}/models"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {get_lm_studio_api_key()}"},
    )

    print(f"Conectando em: {url}")
    print(f"Modelo configurado no .env: {get_lm_studio_model_id()!r}\n")

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print("ERRO: não foi possível conectar ao LM Studio.")
        print(f"  Detalhe: {e}")
        print("\nConfira:")
        print("  1. LM Studio está aberto")
        print("  2. O modelo está carregado")
        print("  3. O servidor local está ligado (Start Server)")
        print(f"  4. A URL no .env está correta: {base}")
        return 1

    models = data.get("data", [])
    if not models:
        print("Servidor respondeu, mas nenhum modelo foi listado.")
        return 1

    print("Modelos disponíveis no servidor:")
    ids: list[str] = []
    for m in models:
        mid = m.get("id", "?")
        ids.append(mid)
        marker = "  <-- use este ID no .env" if mid == get_lm_studio_model_id() else ""
        print(f"  - {mid}{marker}")

    if get_lm_studio_model_id() not in ids:
        print(
            "\nAVISO: LM_STUDIO_MODEL_ID no .env não coincide com nenhum ID listado."
        )
        print("Copie um dos IDs acima para LM_STUDIO_MODEL_ID no arquivo .env")
        return 1

    print("\nOK: servidor acessível e modelo configurado encontrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
