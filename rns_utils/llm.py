from openai import OpenAI, AsyncOpenAI, OpenAIError
import os
from dotenv import load_dotenv
#import asyncio

load_dotenv()

#API_LIST = os.getenv('API_LIST','')

class Pooling():
    def __init__(self, API_LIST, BASE_URL):
        self.api = API_LIST
        self.idx = 0
        self.list_len = len(API_LIST)
        self.base_url = BASE_URL
        self.client = []

        if(self.list_len == 0):
            raise OpenAIError("API_List is empty, please check your environment variable.")

        for _ in self.api:
            client = OpenAI(
                api_key=_,
                base_url=self.base_url,
            )
            self.client.append(client)

    def call_llm_core(self, prompt, instruction = "Your are an AI assistant.",**kwargs):
        response = self.client[self.idx].chat.completions.create(
            model=os.getenv('MODEL_NAME'),
            messages=[{"role":"system", "content": instruction}, {"role": "user", "content": prompt}],
            temperature=0.7
        )

        self.idx = (self.idx + 1) % self.list_len

        return response.choices[0].message.content

    def call_llm_stream_core(self, prompt, stream_callback=None, **kwargs):
        response = self.client[self.idx].chat.completions.create(
            model=os.getenv('MODEL_NAME'),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            stream=True
        )

        self.idx = (self.idx + 1) % self.list_len

        full_content = ""
        for chunk in response:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                chunk_content = delta.content
                if stream_callback:
                    stream_callback(chunk_content)
                else:
                    print(chunk_content, end="", flush=True)
                full_content += chunk_content

        if not stream_callback:
            print()

        return full_content

    def pivot(self, func, prompt, instruction, attempt=0, **kwargs):
        attempt = attempt
        try:
            return func(prompt, instruction = instruction, **kwargs)
        except OpenAIError as e:
            attempt += 1
            if (attempt == self.list_len):
                raise OpenAIError("All the API keys are unavailable, stop running")
            print(f"Call API key {self.idx} fails. Error：{e}")
            print(("Call the next API key"))
            self.idx = (self.idx + 1) % self.list_len
            return self.pivot(func, prompt, instruction = instruction, attempt=attempt, **kwargs)

    def call_llm(self, prompt, instruction = "You are an AI assistant.", stream=True, stream_callback=None):
        if stream:
            return self.pivot(func=self.call_llm_stream_core, prompt=prompt, instruction = instruction, stream_callback=stream_callback)
        return self.pivot(func=self.call_llm_core, prompt=prompt)

if __name__ == "__main__":
    base_url = os.getenv("BASE_URL", "")
    api_keys_string = os.getenv("API_LIST", [])
    api_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]
    pooling = Pooling(API_LIST=api_list, BASE_URL=base_url)

    pooling.call_llm("Use 50 words to describe Genshin Impact")
