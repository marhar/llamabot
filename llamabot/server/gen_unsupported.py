#!/usr/bin/env python
"""Generate unsupported API endpoints for llamabot."""

unsupported_delete_cmds = ["delete"]
unsupported_get_cmds = ["tags"]
unsupported_post_cmds = [
    "blobs",
    "chat",
    "copy",
    "create",
    "embeddings",
    "pull",
    "push",
    "show",
]


def gen(method: str, cmd: str) -> None:
    print("")
    print("")
    print(f'@app.{method}("/api/{cmd}")')
    print(f"def unsupported_app_{cmd}():")
    print(f'    """Autogenerated by gen_unsupported.py"""')
    print(f"    raise fastapi.HTTPException(")
    print(f"        status_code=fastapi.status.HTTP_501_NOT_IMPLEMENTED,")
    print(f'        detail=f"unsupported endpoint: {cmd}",')
    print(f"    )")


for cmd in unsupported_delete_cmds:
    gen("delete", cmd)

for cmd in unsupported_get_cmds:
    gen("get", cmd)

for cmd in unsupported_post_cmds:
    gen("post", cmd)