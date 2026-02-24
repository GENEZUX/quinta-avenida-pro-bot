import sys
import os

# Agregar el directorio padre al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.content_creator import ContentCreator
from bot.data_analyst import DataAnalyst
from bot.researcher import Researcher
from bot.knowledge_base import KnowledgeBase

def run_daily_tasks(ollama_url="http://localhost:11434"):
    print("[ANDROMEDA] Iniciando automatizaciones diarias de Quinta Avenida Pro...")
    print("=" * 60)

    try:
        # FASE 1: Investigacion
        print("\n[FASE 1] Investigacion con Ollama...")
        researcher = Researcher(ollama_url)
        topic = "Nuevas herramientas de IA para marketing digital en 2025"
        research = researcher.research_topic(topic)
        print(f"Investigacion completada: {len(research)} caracteres")

        # FASE 2: Analisis
        print("\n[FASE 2] Analisis de datos...")
        analyst = DataAnalyst(ollama_url)
        analysis = analyst.analyze_data(research[:500] if len(research) > 500 else research)
        print(f"Analisis completado: {len(analysis)} caracteres")

        # FASE 3: Creacion de Contenido
        print("\n[FASE 3] Creacion de contenido...")
        creator = ContentCreator(ollama_url)
        post = creator.generate_content(f"Post para redes sociales basado en: {analysis[:300]}")
        print(f"Contenido generado: {len(post)} caracteres")

        # FASE 4: Base de Conocimientos
        print("\n[FASE 4] Guardando en Knowledge Base...")
        kb = KnowledgeBase()
        kb.add_info("last_research", research)
        kb.add_info("last_analysis", analysis)
        kb.add_info("last_content_post", post)
        print("Base de conocimientos actualizada.")

        print("\n[ANDROMEDA] TODAS LAS TAREAS COMPLETADAS CON EXITO")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    success = run_daily_tasks(ollama_host)
    sys.exit(0 if success else 1)
