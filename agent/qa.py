from openai import OpenAI

from agent.config import CHAT_MODEL
from agent.prompts.qa_prompt import QA_PROMPT

client = OpenAI()

class QAService:
    def answer(self, context:str, question:str):

        prompt = f"""
You are a document assistant.

Answer ONLY from the provided context.

If the answer does not exist,
say:

"I could not find this information in the document."

Context:

{context}

Question:

{question}
"""
        response = (
            client.responses.create(
                model=CHAT_MODEL,
                input=prompt,
            )
        )

        return response.output_text

def answer_question(context:str, question:str):

    response = client.responses.create(
        model=CHAT_MODEL,
        input=QA_PROMPT.format(context=context, question=question)
    )

    return response.output_text