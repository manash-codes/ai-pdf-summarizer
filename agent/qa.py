from openai import OpenAI

from agent.prompts.qa_prompt import QA_PROMPT

client = OpenAI()

def answer_question(context:str, question:str):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=QA_PROMPT.format(context=context, question=question)
    )

    return response.output_text