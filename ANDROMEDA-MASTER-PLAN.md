# ANDROMEDA MASTER PLAN - QUINTA AVENIDA PRO
## Genesis MetaWorks | Puerto Rico | 2025

---

## VISION GENERAL

Sistema de IA multi-agente totalmente automatizado que opera desde Ollama local,
generando ingresos pasivos para Genesis MetaWorks usando LLMs locales.

---

## ARQUITECTURA DEL SISTEMA

```mermaid
graph TD
    A[ANDROMEDA - IA Maestra] --> B[Researcher Agent]
    A --> C[Data Analyst Agent]
    A --> D[Content Creator Agent]
    A --> E[Knowledge Base]
    B --> F[Ollama Local LLM]
    C --> F
    D --> F
    E --> G[knowledge.json]
    D --> H[Telegram Bot]
    H --> I[Clientes / Leads]
    A --> J[Daily Automations]
    J --> B
    J --> C
    J --> D
```

---

## FLUJO DE TRABAJO DIARIO

```mermaid
sequenceDiagram
    participant A as Andromeda
    participant R as Researcher
    participant D as DataAnalyst
    participant C as ContentCreator
    participant KB as KnowledgeBase
    participant T as Telegram

    A->>R: Investigar tema del dia
    R->>A: Resultados de investigacion
    A->>D: Analizar datos
    D->>A: Insights y recomendaciones
    A->>C: Generar contenido
    C->>A: Post/Contenido listo
    A->>KB: Guardar resultados
    A->>T: Publicar/Notificar
```

---

## FASES DE IMPLEMENTACION

```mermaid
gantt
    title Plan de Implementacion Andromeda
    dateFormat  YYYY-MM-DD
    section Fase 1 - Base
    Agentes Python    :done, 2025-01-01, 2025-01-07
    Ollama Setup      :done, 2025-01-01, 2025-01-03
    section Fase 2 - Integracion
    Telegram Bot      :done, 2025-01-01, 2025-01-10
    Vercel Deploy     :done, 2025-01-01, 2025-01-10
    section Fase 3 - Monetizacion
    Plan $200/mes     :active, 2025-01-10, 2025-02-01
    Clientes PR       :2025-01-15, 2025-03-01
    section Fase 4 - Escala
    Multi-bot         :2025-02-01, 2025-04-01
    Ingresos Pasivos  :2025-03-01, 2025-12-31
```

---

## REPOSITORIOS ACTIVOS

| Bot | Repositorio | Estado |
|-----|-------------|--------|
| Quinta Avenida Pro | quinta-avenida-pro-bot | ACTIVO |
| Kemical Extreme | kemical-extreme-bot | ACTIVO |
| Barbosa Agency | barbosa-agency-pro-bot | ACTIVO |

---

## PARA EJECUTAR LOCALMENTE CON OLLAMA

```powershell
# 1. Asegurate de tener Ollama corriendo
ollama serve

# 2. Pull el modelo si no lo tienes
ollama pull llama3

# 3. Clonar el repo
git clone https://github.com/GENEZUX/quinta-avenida-pro-bot.git
cd quinta-avenida-pro-bot

# 4. Instalar dependencias
pip install requests flask python-telegram-bot

# 5. Ejecutar automatizaciones diarias
$env:OLLAMA_HOST="http://localhost:11434"
python -m bot.daily_automations
```

---

## INGRESOS PROYECTADOS

| Servicio | Precio/mes | Clientes meta |
|---------|-----------|---------------|
| Bot Telegram Pro | $200 | 10 |
| Automatizacion IA | $500 | 5 |
| Consultoria | $1000 | 3 |
| **TOTAL** | **$7500** | **18** |

---

*Generado por Andromeda | Genesis MetaWorks | Puerto Rico 2025*
