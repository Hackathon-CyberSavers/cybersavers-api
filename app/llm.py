from openai import OpenAI


client = OpenAI()


class Llm:
    def __init__(self) -> None:
        pass

    @staticmethod
    def completion(messages):
        return client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

