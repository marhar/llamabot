# Notes

## ollama results

### generate / stream = false

request:
```
PORT=11434 curl -s http://localhost:$PORT/api/generate -d '{
  "model": "llama2",
  "stream": false,
  "prompt": "in 10 words, why do fools fall in love?"
}'
```
response:

```
{
  "model": "llama2",
  "created_at": "2024-02-18T23:23:16.062987Z",
  "response": "\nFools fall in love because they are blinded by emotions.",
  "done": true,
  "context": [ 518, 25580, 29962, 3532, 14816, ...],
  "total_duration": 444870875,
  "load_duration": 470042,
  "prompt_eval_duration": 133508000,
  "eval_count": 16,
  "eval_duration": 310668000
}
```

### generate / stream = true
request:
```
PORT=11434 curl -s http://localhost:$PORT/api/generate -d '{
  "model": "llama2",
  "stream": true,
  "prompt": "in 10 words, why do fools fall in love?"
}'
```
response:

```
{ "model": "llama2", "created_at": "2024-02-18T23:25:49.397167Z", "response": "F", "done": false }
{ "model": "llama2", "created_at": "2024-02-18T23:25:49.415877Z", "response": "ools", "done": false }
...
{
  "model": "llama2",
  "created_at": "2024-02-18T23:25:49.696403Z",
  "response": "",
  "done": true,
  "context": [ 518, 25580, 29962, ...  ],
  "total_duration": 441085584,
  "load_duration": 344584,
  "prompt_eval_duration": 141304000,
  "eval_count": 16,
  "eval_duration": 299209000
}
```
