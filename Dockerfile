FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    OLLAMA_HOST=http://ollama:11434

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY --chown=app:app chatbot.py server.py ollama-chatbot-ui.html requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER app
EXPOSE 8080

CMD ["python", "server.py"]