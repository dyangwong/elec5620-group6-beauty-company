"""Deterministic fixtures. These do not demonstrate live LLM perception or generation."""


class MockLlm:
    simulated = True

    def propose(self, context, evidence):
        if not evidence:
            return {"productId": None, "factRefs": [], "simulated": True}
        product = evidence[0]
        return {
            "productId": product["id"],
            "factRefs": list(product["facts"]),
            "simulated": True,
        }

    def generate_script(self, brief, evidence):
        # The creative brief is stored separately and cannot introduce product facts.
        facts = evidence["facts"]
        return {
            "script": f"Meet {evidence['name']}. " + ". ".join(facts) + ".",
            "claims": list(facts),
            "storyboard": [
                {"shot": 1, "duration": "0–5 s", "caption": evidence["name"], "direction": "Product introduction"},
                {"shot": 2, "duration": "5–10 s", "caption": facts[0], "direction": "Catalogue-supported benefit"},
                {"shot": 3, "duration": "10–15 s", "caption": "Explore the product details", "direction": "Draft closing card"},
            ],
            "simulated": True,
        }


class MockMedia:
    def generate(self, script):
        return {"kind": "MOCK_STORYBOARD", "simulated": True,
                "label": "Storyboard placeholder; no video file has been generated.",
                "frames": script["storyboard"]}
