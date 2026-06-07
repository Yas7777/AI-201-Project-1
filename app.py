import gradio as gr
from generator import ask

theme = gr.themes.Soft(
    primary_hue="pink",
    secondary_hue="pink",
    neutral_hue="pink",
    spacing_size="lg",
    radius_size="lg",
    text_size="lg",
)


def handle_query(question):
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


def clear_fields():
    return "", "", ""


with gr.Blocks(theme=theme) as demo:
    gr.Markdown("## Broadway Q&A\nAsk a question and get sourced Broadway answers.")

    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="Example: Where is The Play That Goes Wrong currently playing?",
            lines=2,
            scale=4,
        )

    with gr.Row():
        btn = gr.Button("Ask", variant="primary", size="lg")
        clear = gr.Button("Clear", variant="secondary", size="lg")

    with gr.Row():
        with gr.Column(scale=3):
            answer = gr.Textbox(
                label="Answer",
                lines=8,
            )

        with gr.Column(scale=2):
            sources = gr.Textbox(
                label="Retrieved from",
                lines=8,
            )

        btn.click(handle_query, inputs=inp, outputs=[answer, sources])
        inp.submit(handle_query, inputs=inp, outputs=[answer, sources])
        clear.click(clear_fields, outputs=[inp, answer, sources])



if __name__ == "__main__":
    demo.launch()