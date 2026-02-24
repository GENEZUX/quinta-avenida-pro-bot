import requests
import json

class Researcher:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url + "/api/generate"

    def research_topic(self, topic, model="llama3"):
        data = {
            "model": model,
            "prompt": f"Realiza una investigacion profunda sobre {topic} relevante para el mercado de Puerto Rico y la automatizacion con IA. Resume los hallazgos clave para Quinta Avenida Pro.",
            "stream": False
        }
        try:
            response = requests.post(self.ollama_url, json=data)
            if response.status_code == 200:
                return response.json().get("response", "")
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error conectando con Ollama: {str(e)}"

if __name__ == "__main__":
    researcher = Researcher()
    print(researcher.research_topic("Tendencias de IA en el Caribe 2025"))
