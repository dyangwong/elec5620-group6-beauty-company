"""Bounded MC text composition. Every promotional claim is catalogue-literal."""
from copy import deepcopy

STYLES = {
    "CALM": ("Slow product close-up on a plain background", "Gentle pan across the evidence caption", "Still closing card"),
    "ENERGETIC": ("Quick product reveal on a plain background", "Bold motion around the evidence caption", "Brisk closing card"),
    "INFORMATIVE": ("Clear product view on a plain background", "Static evidence caption", "Simple closing card"),
}
DURATIONS = ("0–5 s", "5–10 s", "10–15 s")
CTA = "Explore the product details"


def compose(plan, brief, product):
    """Validate model-selected facts/style against independent original evidence."""
    if not isinstance(plan, dict) or set(plan) != {"productId", "style", "briefRef", "factRefs", "featureFact"}:
        raise ValueError("Invalid MC plan schema")
    if plan["productId"] != product["id"] or not isinstance(plan["style"], str) or plan["style"] not in STYLES:
        raise ValueError("Unsupported product or visual style")
    quote = plan["briefRef"]
    if not isinstance(quote, str) or not quote.strip() or len(quote) > 200 or quote not in brief:
        raise ValueError("No literal brief reference")
    refs = plan["factRefs"]
    if (not isinstance(refs, list) or not 1 <= len(refs) <= len(product["facts"])
            or any(not isinstance(fact, str) or fact not in product["facts"] for fact in refs)
            or len(set(refs)) != len(refs)
            or not isinstance(plan["featureFact"], str) or plan["featureFact"] not in refs):
        raise ValueError("Unsupported MC facts")
    captions = (product["name"], plan["featureFact"], CTA)
    return {"script": f"Meet {product['name']}. " + ". ".join(refs) + f". {CTA}.",
            "claims": list(refs), "simulated": False, "textPlan": deepcopy(plan),
            "storyboard": [{"shot": index, "duration": duration, "caption": caption, "direction": direction}
                for index, (duration, caption, direction) in enumerate(zip(DURATIONS, captions, STYLES[plan["style"]]), 1)]}


def validate_live_script(script, brief, product):
    if not isinstance(script, dict) or set(script) != {"script", "claims", "storyboard", "simulated", "textPlan"}:
        raise ValueError("Invalid composed MC schema")
    if script["simulated"] is not False or script != compose(script["textPlan"], brief, product):
        raise ValueError("Actual script/captions differ from independently grounded composition")
