import requests

# Simpele wrapper voor OpenRouter API, gebruikt voor agentic reasoning taken
class OpenRouterLLM:
    def __init__(self, api_key, model="mistralai/mistral-7b-instruct"):
        self.api_key = api_key
        self.model = model
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def complete(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a reasoning agent solving puzzles."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()["choices"][0]["message"]["content"]