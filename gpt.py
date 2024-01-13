# initialize the GPT-4 model
import time

from openai import OpenAI
import os
import tiktoken

client = OpenAI()
client.api_key = os.environ["OPENAI_API_KEY_LATEX"]
client.organization = os.environ["OPENAI_ORGANIZATION"]


def count_token(_text: str) -> int:
    """
    Count the number of tokens in a text.

    :param _text: The text to count the tokens in.
    :return: The number of tokens in the text.
    """
    enc = tiktoken.encoding_for_model("gpt-4")
    return len(enc.encode(_text))


def call(_text: str, _language: str) -> str:
    messages = [{
        "role": "system",
        "content": "Given a scientific master thesis written in LaTeX format, please review and improve the "
                   "text by correcting spelling and grammar errors, implementing an academic writing style, "
                   "and removing redundant sentences or descriptions. Focus on enhancing clarity, coherence, "
                   "and overall quality of the written content. Additionally, ensure that the revised text "
                   "adheres to the conventions and standards of academic writing. Provide detailed and "
                   "insightful edits to enhance the overall readability and professionalism of the document."
                   "The language of the thesis is {}.".format(_language)
    },
        {
            "role": "user",
            "content": _text
        }
    ]

    while True:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=1,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].text
        except Exception as e:
            print(e)
            # wait for 60 seconds
            print("Waiting for 60 seconds...")
            time.sleep(60)


if __name__ == "__main__":
    text = "This is a test."
    print(call(text, "English"))
