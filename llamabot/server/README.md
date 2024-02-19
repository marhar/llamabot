* llamabot\_server -- make a llamabot look like an LLM.

This code implements the `ollama serve` API, allowing a llamabot to be coded that shows
up like a model being served by ollama.

Default ollama port is 11434.


** Usage

** Files

```
json_compare.py          some code to "soft compare" json output
notes.md                 dev notes on api implementation, may go away when complete
null_server.py           server that goes directly to litellm, for reference.
api.md                   api doc
null_server.py           server that just forwards to litellm, for reference.
llamabot_server.py       server code
gen_unsupported.py       generates boilerplate for the unsupported API endpoints.
tests/
```
