# generate, stream=false
# second example from ollama api doc

# TODO: parameterize to be server, streaming, model
# TODO: add check for results correctness
#
PORT=${PORT:-8000}

# STREAM=true/false
# PORT=11434 MODEL=llama2
# PORT=8000 MODEL=ollama/llama2

curl -s http://localhost:$PORT/api/generate -d '{
  "model": "ollama/llama2",
  "stream": false,
  "prompt": "why do fools fall in love? limit your response to 10 words.",
}'
