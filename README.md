# Ollama Web Search Integration for Open WebUI

This project provides a FastAPI proxy that integrates Ollama's Web Search functionality with Open WebUI, allowing you to use web search capabilities directly from your chat interface.

## Prerequisites

- Docker and Docker Compose installed
- Ollama API key (get one from [ollama.com](https://ollama.com))
- A VPS or local machine with Docker support

## Quick Setup

1. **Clone or create the project structure:**
   ```
   ollama-websearch/
   ├─ docker-compose.yml
   ├─ .env
   └─ proxy/
      ├─ Dockerfile
      └─ app.py
   ```

2. **Configure your API key:**
   Edit the `.env` file and replace `YOUR_OLLAMA_API_KEY_HERE` with your actual Ollama API key.

3. **Start the services:**
   ```bash
   cd ollama-websearch
   docker compose up -d
   ```

4. **Verify the setup:**
   - FastAPI proxy docs: http://localhost:8010/docs
   - Open WebUI: http://localhost:3000

5. **Add to Open WebUI:**
   - Go to Open WebUI → Settings → OpenAPI Servers → Add Server
   - URL: `http://localhost:8010` (or your VPS IP with port 8010)
   - Name: "Ollama Web Search"

## Usage

Once configured, you'll have access to two new tools in Open WebUI:

- **web_search**: Search the web for information
- **web_fetch**: Fetch content from a specific URL

## Architecture

- **openwebui**: The main Open WebUI interface (port 3000)
- **ollama-websearch**: FastAPI proxy that forwards requests to Ollama's cloud API (port 8010)

## Security Notes

- Keep your `.env` file private and never commit it to version control
- Consider adding rate limiting for production use
- Use HTTPS in production environments

## Troubleshooting

1. **Check container logs:**
   ```bash
   docker compose logs ollama-websearch
   ```

2. **Test the proxy directly:**
   ```bash
   curl -X POST http://localhost:8010/web_search \
     -H "Content-Type: application/json" \
     -d '{"query": "FastAPI tutorial", "max_results": 3}'
   ```

3. **Verify API key:**
   Make sure your Ollama API key is correctly set in the `.env` file.

## Production Deployment

For production use, consider:
- Using HTTPS with a reverse proxy (Nginx)
- Adding rate limiting
- Implementing proper logging
- Using Docker secrets for the API key