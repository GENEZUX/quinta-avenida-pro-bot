import json
import os

class KnowledgeBase:
    def __init__(self, file_path="knowledge.json"):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "company": "Quinta Avenida Pro",
            "services": [],
            "leads": [],
            "vision": "Liderar la automatizacion con IA en Puerto Rico"
        }

    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def add_info(self, key, value):
        self.data[key] = value
        self.save_data()

    def get_info(self, key):
        return self.data.get(key, None)

if __name__ == "__main__":
    kb = KnowledgeBase()
    kb.add_info("plan", "Andromedas Master Plan 2025")
    print("Base de conocimientos actualizada.")
