import requests
import os

class OllamaWrapper:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def chat(self, prompt):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.model_name, "prompt": prompt}
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"[Ollama Error] {str(e)}"

class HuggingFaceWrapper:
    def __init__(self, model_url, api_token):
        self.model_url = model_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def chat(self, prompt):
        try:
            response = requests.post(
                self.model_url,
                headers=self.headers,
                json={"inputs": prompt}
            )
            response.raise_for_status()
            result = response.json()
            return result[0]["generated_text"].strip() if result and isinstance(result, list) else "[HF Error] Unexpected output format"
        except Exception as e:
            return f"[Hugging Face Error] {str(e)}"
