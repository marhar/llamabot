# chat, stream not specified, therefore true

PORT=${PORT:-8000}

curl -s http://localhost:$PORT/api/chat -d '{
  "model": "llama2",
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    }
  ]
}'
