from openai import OpenAI

from agent.prompts.summary_prompt import SUMMARY_PROMPT

client = OpenAI()

def summarize_document(context:str):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=SUMMARY_PROMPT.format(context=context)
    )

    return response.output_text