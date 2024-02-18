curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{
  "model": "llama2",
  "stream": true,
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    }
  ]
}'
