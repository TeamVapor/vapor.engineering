"""The jam-parcel postmaster: presigned-URL issuer for the relay bucket.

One Lambda, three ops, no accounts, no database. The app never holds AWS
credentials; S3 enforces the size cap via the presigned-POST condition, the
bucket lifecycle enforces the 30-day TTL, and quota is computed by listing
the recipient's mailbox prefix (fine at friend-to-friend scale).

POST JSON to the Function URL:
  {"op": "send",    "to": "<address>", "size_bytes": N}
      -> {"url": ..., "fields": {...}, "key": ...}   (presigned POST)
  {"op": "mailbox", "me": "<address>"}
      -> {"parcels": [{"key", "size", "modified"}]}
  {"op": "fetch",   "key": "mail/<address>/<name>"}
      -> {"get_url": ..., "delete_url": ...}

Addresses: 6-32 chars of A-Z, 2-7, and dashes (crockford-ish, no lookalikes).
"""

import json
import os
import re

import boto3

BUCKET = os.environ["BUCKET"]
MAX_PARCEL_BYTES = int(os.environ.get("MAX_PARCEL_MB", "200")) * 1024 * 1024
QUOTA_BYTES = int(os.environ.get("QUOTA_MB", "1024")) * 1024 * 1024
URL_TTL = int(os.environ.get("URL_TTL_SECONDS", "900"))

ADDRESS = re.compile(r"^[A-Z2-7][A-Z2-7-]{4,30}[A-Z2-7]$")
KEY = re.compile(r"^mail/[A-Z2-7][A-Z2-7-]{4,30}[A-Z2-7]/[\w.-]{1,128}$")

s3 = boto3.client("s3")


def _reply(code, body):
    return {
        "statusCode": code,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def _mailbox_usage(address):
    total, items = 0, []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=f"mail/{address}/"):
        for obj in page.get("Contents", []):
            total += obj["Size"]
            items.append(obj)
    return total, items


def _op_send(req):
    to = req.get("to", "")
    size = int(req.get("size_bytes", 0))
    if not ADDRESS.match(to):
        return _reply(400, {"error": "bad address"})
    if not 0 < size <= MAX_PARCEL_BYTES:
        return _reply(400, {"error": f"size must be 1..{MAX_PARCEL_BYTES} bytes"})
    used, _ = _mailbox_usage(to)
    if used + size > QUOTA_BYTES:
        return _reply(409, {"error": "recipient mailbox quota exceeded",
                            "used_bytes": used, "quota_bytes": QUOTA_BYTES})
    key = f"mail/{to}/{os.urandom(8).hex()}.jamparcel"
    post = s3.generate_presigned_post(
        Bucket=BUCKET,
        Key=key,
        Conditions=[["content-length-range", 1, MAX_PARCEL_BYTES]],
        ExpiresIn=URL_TTL,
    )
    return _reply(200, {"url": post["url"], "fields": post["fields"], "key": key})


def _op_mailbox(req):
    me = req.get("me", "")
    if not ADDRESS.match(me):
        return _reply(400, {"error": "bad address"})
    _, items = _mailbox_usage(me)
    parcels = [{"key": o["Key"], "size": o["Size"],
                "modified": o["LastModified"].isoformat()} for o in items]
    return _reply(200, {"parcels": parcels})


def _op_fetch(req):
    key = req.get("key", "")
    if not KEY.match(key):
        return _reply(400, {"error": "bad key"})
    get_url = s3.generate_presigned_url(
        "get_object", Params={"Bucket": BUCKET, "Key": key}, ExpiresIn=URL_TTL)
    delete_url = s3.generate_presigned_url(
        "delete_object", Params={"Bucket": BUCKET, "Key": key}, ExpiresIn=URL_TTL)
    return _reply(200, {"get_url": get_url, "delete_url": delete_url})


OPS = {"send": _op_send, "mailbox": _op_mailbox, "fetch": _op_fetch}


def handler(event, _context):
    try:
        req = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _reply(400, {"error": "bad json"})
    op = OPS.get(req.get("op", ""))
    if not op:
        return _reply(400, {"error": "unknown op"})
    return op(req)
