"""The feedback scribe: takes {message, name?} from the site, files it in S3.

No accounts, no database. Caps are layered: the Function URL rejects
nothing (anyone can write), but the body must be small JSON, the message
and name have hard length caps, and reserved concurrency 1 throttles the
rate. Worst case abuse is a trickle of tiny objects — pennies.
"""

import json
import os
import time

import boto3

BUCKET = os.environ["BUCKET"]
MAX_BODY_BYTES = 8 * 1024
MAX_MESSAGE_CHARS = 4000
MAX_NAME_CHARS = 64

s3 = boto3.client("s3")


def _reply(code, body):
    return {
        "statusCode": code,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def handler(event, _context):
    body = event.get("body") or ""
    if len(body) > MAX_BODY_BYTES:
        return _reply(413, {"error": "too big"})
    try:
        req = json.loads(body)
    except json.JSONDecodeError:
        return _reply(400, {"error": "bad json"})

    message = str(req.get("message", "")).strip()
    name = str(req.get("name", "")).strip()
    if not message:
        return _reply(400, {"error": "empty message"})
    if len(message) > MAX_MESSAGE_CHARS or len(name) > MAX_NAME_CHARS:
        return _reply(400, {"error": "too long"})

    http = event.get("requestContext", {}).get("http", {})
    now = time.gmtime()
    key = (f"feedback/{now.tm_year}/{now.tm_mon:02}/{now.tm_mday:02}/"
           f"{int(time.time())}-{os.urandom(4).hex()}.json")
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", now),
            "name": name,
            "message": message,
            "ip": http.get("sourceIp", ""),
            "ua": http.get("userAgent", ""),
        }).encode(),
        ContentType="application/json",
    )
    return _reply(200, {"ok": True})
