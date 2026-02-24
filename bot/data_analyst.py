import requests
import json

class DataAnalyst:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url + "/api/generate"

    def analyze_data(self, data_summary, model="llama3"):
        data = {
            "model": model,
            "prompt": f"Analiza los siguientes datos comerciales para Quinta Avenida Pro y proporciona insights clave y recomendaciones: {data_summary}",
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
    analyst = DataAnalyst()
    print(analyst.analyze_data("Ventas enero: $5000, Leads: 150, Conversion: 3%"))
