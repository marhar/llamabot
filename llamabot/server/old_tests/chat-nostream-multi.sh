# chat, stream not specified, therefore true

PORT=${PORT:-8000}

curl -s http://localhost:$PORT/api/chat -d '{
  "model": "llama2",
  "messages": [
    {
      "role": "user",
      "content": "what is the weather like?"
    },
    {
      "role": "assistant",
      "content": "it is sunny."
    },
    {
      "role": "user",
      "content": "why does it rain?"
    },
    {
      "role": "assistant",
      "content": "water in the sky."
    },
    {
      "role": "user",
      "content": "why is the sky blue?"
    }
  ],
  "stream": false
}'
