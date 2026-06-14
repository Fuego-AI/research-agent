"""
Fuego AI - Mystical Deep Research Interface
Versão Estabilizada e Verificada para Gradio 6.0+
"""

from __future__ import annotations

import gradio as gr
import os
from pathlib import Path

from agent import research_agent
from config import get_gradio_server_port, get_gradio_share

# --- Configurações de Identidade ---
LOGO_PATH = "Fuego_AI/Fueguito nino.jpeg"

# --- CSS Místico e Elegante ---
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');

:root {
    --fuego-deep-bg: #050505;
    --fuego-card-bg: #0a0a0a;
    --fuego-accent: #ff4d00;
    --fuego-accent-glow: rgba(255, 77, 0, 0.2);
    --fuego-text: #d1d1d1;
    --fuego-text-dim: #888;
}

body, .gradio-container {
    background-color: var(--fuego-deep-bg) !important;
    color: var(--fuego-text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

footer {visibility: hidden}

.main-wrap {
    max-width: 900px !important;
    margin: 0 auto !important;
    padding-top: 5vh !important;
}

#welcome-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 40vh;
    text-align: center;
}

#welcome-section img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    filter: drop-shadow(0 0 20px var(--fuego-accent-glow));
    margin-bottom: 1.5rem;
    border: 1px solid var(--fuego-accent);
    object-fit: cover;
}

#welcome-section h1 {
    font-size: 2.5rem;
    font-weight: 300;
    background: linear-gradient(to right, #ff8c00, #ff4d00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

#chatbot-wrap {
    background: transparent !important;
    border: none !important;
}

.message.user {
    background: var(--fuego-card-bg) !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 20px 20px 4px 20px !important;
}

#input-box {
    position: fixed !important;
    bottom: 40px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 85% !important;
    max-width: 800px !important;
    background: rgba(15, 15, 15, 0.8) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 77, 0, 0.1) !important;
    border-radius: 30px !important;
    padding: 8px 15px !important;
    z-index: 1000;
}

#input-box textarea {
    background: transparent !important;
    border: none !important;
    color: white !important;
    box-shadow: none !important;
}

#send-btn {
    background: var(--fuego-accent) !important;
    color: white !important;
    border-radius: 50% !important;
    min-width: 42px !important;
    max-width: 42px !important;
    height: 42px !important;
    border: none !important;
    font-size: 20px !important;
}

.suggestion-btn {
    background: #0f0f0f !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 12px !important;
    color: var(--fuego-text-dim) !important;
    margin: 5px !important;
}
"""

EXAMPLES = [
    "Quais os mistérios da IA para 2026?",
    "O que eu posso aprender com você?.",
    "O que a neurociência diz sobre a intuição?",
]

async def stream_from_agent(
    prompt: str,
    chatbot: list[dict],
    past_messages: list,
):
    if not prompt or not prompt.strip():
        yield gr.update(interactive=True), chatbot, past_messages, gr.update(visible=True)
        return

    chatbot.append({"role": "user", "content": prompt})
    yield gr.update(value="", interactive=False), chatbot, gr.skip(), gr.update(visible=False)
 
    try:
        async with research_agent.run_stream(
            prompt.strip(),
            message_history=past_messages,
        ) as result:
            chatbot.append({"role": "assistant", "content": ""})
            async for text in result.stream_text():
                chatbot[-1]["content"] = text
                yield gr.skip(), chatbot, gr.skip(), gr.update(visible=False)

            past_messages = result.all_messages()
    except Exception as e:
        chatbot.append({"role": "assistant", "content": f"Ocorreu um erro na chama: {e}"})
        yield gr.skip(), chatbot, gr.skip(), gr.update(visible=False)

    yield gr.update(interactive=True, placeholder="Pergunte ao Fuego..."), gr.skip(), past_messages, gr.update(visible=False)

def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Fuego AI") as demo:
        
        with gr.Column(elem_classes="main-wrap"):
            
            # Seção de Boas-Vindas
            with gr.Column(elem_id="welcome-section") as welcome_box:
                if os.path.exists(LOGO_PATH):
                    gr.Image(LOGO_PATH, show_label=False, container=False, width=120)
                gr.Markdown("# Fuego AI")
                gr.Markdown("Entre na chama do conhecimento profundo.")
                
                with gr.Row():
                    for ex in EXAMPLES:
                        gr.Button(ex, elem_classes="suggestion-btn").click(
                            lambda x=ex: x, outputs=[gr.State(ex)]
                        )

            past_messages = gr.State([])
            
            # Chatbot (Simplificado para Gradio 6.0+)
            chatbot = gr.Chatbot(
                elem_id="chatbot-wrap",
                avatar_images=(None, LOGO_PATH if os.path.exists(LOGO_PATH) else None),
            )

            # Input Box
            with gr.Row(elem_id="input-box"):
                prompt = gr.Textbox(
                    lines=1,
                    show_label=False,
                    placeholder="Inicie a conversa...",
                    scale=20,
                )
                send_btn = gr.Button("↑", elem_id="send-btn", scale=1)

            # --- Interações ---
            input_params = [prompt, chatbot, past_messages]
            output_params = [prompt, chatbot, past_messages, welcome_box]

            send_btn.click(stream_from_agent, inputs=input_params, outputs=output_params)
            prompt.submit(stream_from_agent, inputs=input_params, outputs=output_params)

            gr.Examples(
                examples=EXAMPLES,
                inputs=prompt,
                label=None,
                cache_examples=False,
            )

    return demo

if __name__ == "__main__":
    demo = build_ui()
    # Padrão Gradio 6.0: css e theme passados apenas no launch()
    # Se server_port for None, o Gradio encontrará uma porta livre automaticamente
    demo.launch(
        server_port=get_gradio_server_port(),
        share=get_gradio_share(),
        theme=gr.themes.Default(),
        css=CUSTOM_CSS,
        allowed_paths=["Fuego_AI/"]
    )
