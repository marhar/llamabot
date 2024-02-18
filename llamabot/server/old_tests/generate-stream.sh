# generate, stream not specified, therefore true
# second example from ollama api doc

PORT=${PORT:-8000}

curl -s http://localhost:$PORT/api/generate -d '{
  "model": "openai/gpt-4",
  "prompt": "why do fools fall in love?"
}'
