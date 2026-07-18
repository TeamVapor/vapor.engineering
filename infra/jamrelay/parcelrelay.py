"""Jam-parcel relay client: talk to the postmaster, never hold AWS creds.

The seam Jack's jam-mates UX calls (music-as-code #26/#39). Four verbs:

    addr = new_address()                       # your jam address, once, saved in config
    send(relay_url, path, to_address)          # -> parcel key
    parcels = mailbox(relay_url, my_address)   # -> [{key, size, modified}]
    fetch(relay_url, key, dest_dir)            # -> downloaded Path (and drains the mailbox)

Manual exchange (v1: copy the .jamparcel file over any channel) remains the
no-server fallback and privacy opt-out; this module is only the postage.
stdlib-only on purpose.
"""

from __future__ import annotations

import json
import secrets
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

# no lookalike characters; must stay a subset of the postmaster's [A-Z2-7]
_ALPHABET = "ABCDEFGHJKMNPQRSTVWXYZ234567"


def new_address() -> str:
    """Mint a jam address, e.g. 'K7MW-Q2ZC-4VXH'. No registry: you ARE the record."""
    chars = [secrets.choice(_ALPHABET) for _ in range(12)]
    return "-".join("".join(chars[i:i + 4]) for i in (0, 4, 8))


def _post(relay_url: str, payload: dict) -> dict:
    req = urllib.request.Request(
        relay_url,
        data=json.dumps(payload).encode(),
        headers={"content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def send(relay_url: str, path: str | Path, to_address: str) -> str:
    """Upload a parcel to a friend's mailbox. Returns the parcel key."""
    path = Path(path)
    data = path.read_bytes()
    grant = _post(relay_url, {"op": "send", "to": to_address,
                              "size_bytes": len(data)})
    if "error" in grant:
        raise RuntimeError(f"relay refused: {grant['error']}")

    # multipart/form-data POST to S3 with the presigned fields, file last
    boundary = uuid.uuid4().hex
    parts = []
    for name, value in grant["fields"].items():
        parts.append(
            f"--{boundary}\r\ncontent-disposition: form-data; "
            f'name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append(
        f"--{boundary}\r\ncontent-disposition: form-data; name=\"file\"; "
        f'filename="{path.name}"\r\n'
        f"content-type: application/octet-stream\r\n\r\n".encode())
    body = b"".join(parts) + data + f"\r\n--{boundary}--\r\n".encode()

    up = urllib.request.Request(
        grant["url"], data=body, method="POST",
        headers={"content-type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(up, timeout=120) as resp:
        if resp.status not in (200, 201, 204):
            raise RuntimeError(f"upload failed: HTTP {resp.status}")
    return grant["key"]


def mailbox(relay_url: str, my_address: str) -> list[dict]:
    """List parcels waiting at my address."""
    got = _post(relay_url, {"op": "mailbox", "me": my_address})
    if "error" in got:
        raise RuntimeError(f"relay refused: {got['error']}")
    return got["parcels"]


def fetch(relay_url: str, key: str, dest_dir: str | Path) -> Path:
    """Download a parcel to dest_dir and delete it from the relay."""
    grant = _post(relay_url, {"op": "fetch", "key": key})
    if "error" in grant:
        raise RuntimeError(f"relay refused: {grant['error']}")
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    dest = Path(dest_dir) / Path(urllib.parse.urlparse(key).path).name
    with urllib.request.urlopen(grant["get_url"], timeout=120) as resp:
        dest.write_bytes(resp.read())
    req = urllib.request.Request(grant["delete_url"], method="DELETE")
    with urllib.request.urlopen(req, timeout=30):
        pass
    return dest


if __name__ == "__main__":
    import argparse
    import os

    ap = argparse.ArgumentParser(description="jam-parcel relay client")
    ap.add_argument("--relay", default=os.environ.get("JAMRELAY_URL"),
                    help="postmaster function URL (or JAMRELAY_URL env)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("address", help="mint a new jam address")
    p = sub.add_parser("send"); p.add_argument("file"); p.add_argument("--to", required=True)
    p = sub.add_parser("mailbox"); p.add_argument("--me", required=True)
    p = sub.add_parser("fetch"); p.add_argument("key"); p.add_argument("--dest", default=".")
    a = ap.parse_args()

    if a.cmd == "address":
        print(new_address())
    elif a.cmd == "send":
        print(send(a.relay, a.file, a.to))
    elif a.cmd == "mailbox":
        for p in mailbox(a.relay, a.me):
            print(f'{p["size"]:>10}  {p["modified"]}  {p["key"]}')
    elif a.cmd == "fetch":
        print(fetch(a.relay, a.key, a.dest))
