# generate, stream=false
# second example from ollama api doc

# TODO: parameterize to be server, streaming, model
# TODO: add check for results correctness
#
PORT=${PORT:-8000}

if [ $1. = a. ]; then
  PORT=11434
  MODEL=llama2
elif [ $1. = b. ]; then
  PORT=8000
  MODEL=ollama/llama2
elif [ $1. = c. ]; then
  PORT=8000
  MODEL=mistral/mistral-medium
else
  echo "Usage: $0 a|b|c"
  exit 1
fi

curl -s http://localhost:$PORT/api/generate -d '{
  "model": "'$MODEL'",
  "stream": false,
  "prompt": "why do fools fall in love? limit your response to 10 words."
}'
echo
