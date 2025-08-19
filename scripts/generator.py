# -*- coding: utf-8 -*-
import os
import json
import datetime

print("✅ Generator script started at", datetime.datetime.now())

# Fail fast if the env-var is missing
raw = os.getenv("GOOGLE_CREDENTIALS")
if not raw:
    raise SystemExit("❌  GOOGLE_CREDENTIALS env-var is empty or missing!")

# Parse and save
creds = json.loads(raw)
with open("service_account.json", "w") as f:
    json.dump(creds, f)

print("✅ service_account.json written")
