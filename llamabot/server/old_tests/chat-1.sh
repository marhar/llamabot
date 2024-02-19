curl -s -X POST http://localhost:8000/api/generate -H "Content-Type: application/json" -d '{
  "model": "llama2",
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    }
  ]
}'|jq

