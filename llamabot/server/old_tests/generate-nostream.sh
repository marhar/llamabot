# generate, stream=false
# second example from ollama api doc

PORT=${PORT:-8000}

curl -s http://localhost:$PORT/api/generate -d '{
  "model": "openai/gpt-4",
  "stream": false,
  "prompt": "why is the sky blue?"
}'
