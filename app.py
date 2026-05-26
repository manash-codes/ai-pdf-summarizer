import gradio as gr

from agent.services.document_service import (
    DocumentService,
)

from agent.services.session_service import (
    SessionService,
)

from agent.services.chat_service import (
    ChatService,
)


document_service = DocumentService()
session_service = SessionService()
chat_service = ChatService()


def create_session():
    return session_service.create_session()


def upload_document(
    file,
    session_id,
):
    if file is None:
        return (
            None,
            "Please upload a PDF file.",
        )

    result = document_service.process_document(
        file.name
    )

    document_id = result["document_id"]

    session_service.attach_document(
        session_id=session_id,
        document_id=document_id,
    )

    status = f"""
Document Ready

Document ID:
{document_id}

Status:
{result["status"]}

Pages:
{result.get("pages", "-")}

Chunks:
{result.get("chunks", "-")}
"""

    return (
        document_id,
        status,
    )


def generate_summary(
    document_id,
):
    if not document_id:
        return (
            "Please upload a PDF first."
        )

    result = chat_service.ask(
        question="Provide a comprehensive summary of this document.",
        document_id=document_id,
    )

    return result["answer"]


def ask_question(
    message,
    history,
    session_id,
    document_id,
):
    if not document_id:
        history.append(
            {
                "role": "assistant",
                "content": (
                    "Please upload a PDF first."
                ),
            }
        )

        return (
            "",
            history,
        )

    result = chat_service.ask(
        question=message,
        document_id=document_id,
    )

    answer = result["answer"]

    sources = result["sources"]

    if sources:
        answer += (
            "\n\nSources: "
            + ", ".join(
                str(page)
                for page in sources
            )
        )

    session_service.add_message(
        session_id=session_id,
        role="user",
        content=message,
    )

    session_service.add_message(
        session_id=session_id,
        role="assistant",
        content=answer,
    )

    history.append(
        {
            "role": "user",
            "content": message,
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    return (
        "",
        history,
    )


with gr.Blocks(
    title="PDF Chat Assistant"
) as demo:

    gr.Markdown(
        """
# PDF Chat Assistant

Upload a PDF, automatically index it,
and ask questions about its contents.
"""
    )

    session_state = gr.State(
        value=create_session()
    )

    document_state = gr.State()

    with gr.Row():

        with gr.Column(scale=1):

            pdf_file = gr.File(
                label="Upload PDF",
                file_types=[".pdf"],
            )

            status_box = gr.Textbox(
                label="Document Status",
                lines=10,
            )

        with gr.Column(scale=2):

            chatbot = gr.Chatbot(
                label="Chat",
                height=360,
            )

            msg = gr.Textbox(
                label="Ask a Question",
                placeholder=(
                    "What is this document about?"
                ),
            )

            send_btn = gr.Button(
                "Send"
            )
        
        with gr.Column(scale=1):
            summary_output = gr.Textbox(
                label="Summary",
                lines=15,
            )
            
            summary_btn = gr.Button(
                "Generate Summary"
            )


    pdf_file.upload(
        fn=upload_document,
        inputs=[
            pdf_file,
            session_state,
        ],
        outputs=[
            document_state,
            status_box,
        ],
    )

    summary_btn.click(
        fn=generate_summary,
        inputs=[
            document_state,
        ],
        outputs=[
            summary_output,
        ],
    )

    send_btn.click(
        fn=ask_question,
        inputs=[
            msg,
            chatbot,
            session_state,
            document_state,
        ],
        outputs=[
            msg,
            chatbot,
        ],
    )

    msg.submit(
        fn=ask_question,
        inputs=[
            msg,
            chatbot,
            session_state,
            document_state,
        ],
        outputs=[
            msg,
            chatbot,
        ],
    )


if __name__ == "__main__":
    demo.launch()