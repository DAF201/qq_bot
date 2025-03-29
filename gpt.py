import openai
from collections import deque

class GPT:
    def __init__(
        self,
        api_key,
        model="gpt-3.5-turbo",
        GPT_role="You are Terada Tera, an artist from Japan. You will answer all question about you and your arts from your fans. "
        "Also, you will be given a chat history to assist you"
        "You should react as a human and you are answering qustions continuesly even you didn't realized that. "
        "Just answer the question, do not include any reduant things."
        # "You are prefering replying with Japanese but also okay to answer in other languages if they keep the consistancy"
        "You can temporary change your role if required to do so."
        "You are allowed to use any language to keep the conversation consistancy if asked to but your fav is Japanese",
    ):
        # self.api_key = api_key

        self.GPT_role = GPT_role
        self.model = model
        self.chat_history = deque(maxlen=10)
        with open(api_key) as tk:
            openai.api_key = tk.read()

    def ask(self, prompt):
        c = []
        c.append({"role": "user", "content": prompt})
        reply = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.GPT_role},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": str(list(self.chat_history))},
            ],
        )["choices"][0]["message"]["content"]
        c.append({"role": "system", "content": reply})
        self.chat_history.append(c)
        return reply
