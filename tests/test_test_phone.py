"""Which test login each persona gets (scripts/test_phone.py)."""
import json
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from test_phone import phone_for  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST = ",".join(f"+234800000{n:04d}" for n in range(101, 121))


class TestPhone(unittest.TestCase):
    def setUp(self):
        self.personas = json.loads((ROOT / "personas.json").read_text(encoding="utf-8"))

    def test_a_persona_with_a_phone_keeps_it(self):
        self.assertEqual(phone_for("kunle", ALLOWLIST, self.personas), "+2348000000115")

    def test_no_persona_without_a_phone_gets_a_number_another_persona_names(self):
        named = {p["phone"] for p in self.personas if p.get("phone")}
        for p in self.personas:
            if p.get("phone"):
                continue
            with self.subTest(persona=p["id"]):
                self.assertNotIn(phone_for(p["id"], ALLOWLIST, self.personas), named)

    def test_an_allowlist_of_only_named_numbers_still_gives_a_number(self):
        named = sorted({p["phone"] for p in self.personas if p.get("phone")})
        self.assertIn(phone_for("bisi", ",".join(named), self.personas), named)


if __name__ == "__main__":
    unittest.main()
