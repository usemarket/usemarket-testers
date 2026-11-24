"""The test login phone for one persona.

Usage: python3 scripts/test_phone.py <persona id> <TEST_PHONE_ALLOWLIST>
A persona with a "phone" in personas.json (a vendor or rider persona naming
the staging account of its app) uses it. Every other persona takes a number
from the allowlist by its place in personas.json, skipping the numbers any
persona names: a code request cancels every other open code for the same
number, so a customer tester on a vendor tester's number would refuse its
sign-ins (and the other way round).
"""
import json
import sys
from pathlib import Path


def phone_for(persona, allowlist, personas):
    ids = [p["id"] for p in personas]
    me = personas[ids.index(persona)]
    if me.get("phone"):
        return me["phone"]
    named = {p["phone"] for p in personas if p.get("phone")}
    phones = [x.strip() for x in allowlist.split(",") if x.strip()]
    pool = [x for x in phones if x not in named] or phones
    return pool[ids.index(persona) % len(pool)]


if __name__ == "__main__":
    personas = json.loads((Path(__file__).resolve().parent.parent / "personas.json").read_text(encoding="utf-8"))
    print(phone_for(sys.argv[1], sys.argv[2], personas))
