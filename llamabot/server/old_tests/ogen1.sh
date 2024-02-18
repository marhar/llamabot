curl -s http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "stream": false,
  "prompt": "Why is the sky blue?"
}'|jq

