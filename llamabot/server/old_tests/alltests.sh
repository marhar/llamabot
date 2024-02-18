PORT=${PORT:-8000}

for stream in false true; do
    echo chat stream=$stream -------------------------------------------------------
    curl http://localhost:$PORT/api/chat -d '{
      "model": "llama2",
      "stream": '$stream',
      "messages": [
        {
          "role": "user",
          "content": "why is the sky blue?"
        }
      ]
    }'
    echo ''
done

for stream in false true; do
    echo generate stream=$stream -------------------------------------------------------
    curl -s http://localhost:$PORT/api/generate -d '{
      "model": "llama2",
      "stream": '$stream',
      "prompt": "why is the sky blue?"
    }'
    echo ''
done
