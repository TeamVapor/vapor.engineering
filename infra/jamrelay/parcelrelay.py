"""Parcel relay client: mail `.jamparcel` files through the drop bucket.

The v1.5 transport from studio/docs/JAM-ROOMS.md, productized (issue #24,
charter #39 pillar 2): a dumb S3 relay fronted by one Lambda ("the
postmaster") that issues presigned URLs. This module is the app's whole
relationship with it — four verbs, no AWS credentials anywhere:

    addr = new_address()                      # mint once, keep in config
    key  = send(relay_url, path, to_address)  # mail a parcel to a friend
    lst  = mailbox(relay_url, my_address)     # what's waiting for me?
    path = fetch(relay_url, key, dest_dir)    # download + drain from relay

Design stances (Eli's ratified #24 answers): no accounts — an address is
client-minted, given to friends like a phone number, and the friend list
is just "addresses I exchange with"; the relay is a mailbox with a 30-day
TTL, never a home — a fetched parcel is deleted from the bucket and media
lives on player disks; manual exchange of the `.jamparcel` file (Discord,
USB stick) remains the no-server fallback and the privacy opt-out. This
module is only postage: parcel contents are `jamparcel.py`'s business.

The postmaster enforces the caps (size via a presigned-POST condition,
per-mailbox quota, 30-day expiry); infra + ops doc live in the
vapor.engineering repo under `infra/jamrelay/`. The relay URL is config,
not code — it changes once when the relay moves to the company AWS
account, and nothing here notices.

GUI-independent, stdlib-only (urllib + secrets), so WSL tests cover it.
"""

from __future__ import annotations

import json
import secrets
import urllib.parse
import urllib.request
from pathlib import Path

# Address alphabet: crockford-ish base32, no lookalikes (0/O, 1/I/L, 8/B).
# Must stay a subset of the postmaster's accepted [A-Z2-7] class.
_ALPHABET = "ACDEFGHJKMNPQRSTVWXYZ234567"

# test seam: monkeypatch this to fake the network
_open = urllib.request.urlopen


def new_address() -> str:
    """Mint a jam address, e.g. 'K7MW-Q2ZC-4VXH'. No registry: telling a
    friend your address IS the registration."""
    chars = [secrets.choice(_ALPHABET) for _ in range(12)]
    return "-".join("".join(chars[i:i + 4]) for i in (0, 4, 8))


class RelayError(RuntimeError):
    """The postmaster refused (bad address, quota exceeded, ...)."""


def _post(relay_url: str, payload: dict) -> dict:
    req = urllib.request.Request(
        relay_url,
        data=json.dumps(payload).encode(),
        headers={"content-type": "application/json"},
        method="POST",
    )
    with _open(req, timeout=30) as resp:
        got = json.loads(resp.read())
    if "error" in got:
        raise RelayError(got["error"])
    return got


def send(relay_url: str, path: str | Path, to_address: str) -> str:
    """Upload a parcel into a friend's mailbox. Returns the relay key.

    The postmaster checks the recipient's quota and returns a presigned
    S3 POST; the size cap is enforced by S3 itself via the POST condition,
    so a lying client gains nothing.
    """
    path = Path(path)
    data = path.read_bytes()
    grant = _post(relay_url, {"op": "send", "to": to_address,
                              "size_bytes": len(data)})

    # multipart/form-data to S3: presigned fields first, file last
    boundary = secrets.token_hex(16)
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
    with _open(up, timeout=120) as resp:
        if resp.status not in (200, 201, 204):
            raise RelayError(f"upload failed: HTTP {resp.status}")
    return grant["key"]


def mailbox(relay_url: str, my_address: str) -> list[dict]:
    """List parcels waiting at my address: [{key, size, modified}, ...]."""
    return _post(relay_url, {"op": "mailbox", "me": my_address})["parcels"]


def fetch(relay_url: str, key: str, dest_dir: str | Path) -> Path:
    """Download a parcel to dest_dir, then delete it from the relay
    (mailboxes drain when read — the bucket is never a home)."""
    grant = _post(relay_url, {"op": "fetch", "key": key})
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    dest = Path(dest_dir) / Path(urllib.parse.urlparse(key).path).name
    with _open(grant["get_url"], timeout=120) as resp:
        dest.write_bytes(resp.read())
    req = urllib.request.Request(grant["delete_url"], method="DELETE")
    with _open(req, timeout=30):
        pass
    return dest


if __name__ == "__main__":
    import argparse
    import os

    ap = argparse.ArgumentParser(description="jam-parcel relay client")
    ap.add_argument("--relay", default=os.environ.get("JAMRELAY_URL"),
                    help="postmaster URL (or JAMRELAY_URL env)")
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
        for m in mailbox(a.relay, a.me):
            print(f'{m["size"]:>10}  {m["modified"]}  {m["key"]}')
    elif a.cmd == "fetch":
        print(fetch(a.relay, a.key, a.dest))
