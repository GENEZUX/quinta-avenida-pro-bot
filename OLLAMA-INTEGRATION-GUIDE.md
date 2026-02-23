# Guía de Integración Ollama Local

Para usar tu PC local como el cerebro de los bots creados hoy, sigue estos pasos:

## 1. Configurar Ollama
Asegúrate de que Ollama esté instalado y corriendo en tu PC.
Descarga el modelo deseado (ej. llama3):
`ollama run llama3`

## 2. Exponer la API Local
Usa Ngrok para exponer el puerto 11434:
`ngrok http 11434`
Copia la URL generada.

## 3. Configurar Vercel
Añade `OLLAMA_BASE_URL` y `OLLAMA_MODEL` en el panel de Vercel.

---
*Genesis MetaWorks*
