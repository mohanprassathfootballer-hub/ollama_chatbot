# Chat Bot

A local web UI for Ollama, with a small same-origin API proxy so the browser does not need direct Ollama access or CORS configuration.

## Run locally

Install the Python dependency and make sure Ollama is running with the `llama3.2` model installed:

```powershell
py -m pip install -r requirements.txt
py server.py
```

Open <http://127.0.0.1:8080>. Set `OLLAMA_HOST` if Ollama is not at `http://localhost:11434`. The terminal chatbot is also available with `py chatbot.py`.

## Run with Docker

Build and run the web app alongside an Ollama instance:

```sh
docker build -t chat-bot .
docker run --rm -p 8080:8080 -e OLLAMA_HOST=http://host.docker.internal:11434 chat-bot
```

Open <http://127.0.0.1:8080>. For cloud deployment, configure `OLLAMA_HOST` to the private URL of a separately hosted Ollama service and set the container port to `8080`. This image contains the app, not the model; Ollama must have `llama3.2` installed.

## Publish the image

Pushing to `main` runs the GitHub Actions workflow that builds and publishes `ghcr.io/mohanprassathfootballer-hub/ollama_chatbot:latest`. After the first publish, check the package settings in GitHub and make it public or configure registry credentials for your cloud provider.

The UI has no built-in login. Put it behind your cloud provider's authentication or a private network before exposing it publicly.
