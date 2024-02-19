# generate-nostream
# second example from ollama api doc

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
STREAM=false

curl -s http://localhost:$PORT/api/generate -d '{
  "model": "'$MODEL'",
  "stream": '$STREAM',
  "prompt": "why do fools fall in love? response in 10 words or less."
}'
echo
