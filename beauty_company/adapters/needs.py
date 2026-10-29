"""Bounded BA extraction schema; quoted hypotheses still require Customer review."""
import math
import re

FIELDS = ("concern", "budget", "fragranceFree")


def validate_extraction(value, messages):
    if (not isinstance(value, dict) or set(value) != {*FIELDS, "sources"}
            or not isinstance(value["sources"], dict) or set(value["sources"]) != set(FIELDS)):
        raise ValueError("Invalid needs schema")
    result = {key: value[key] for key in FIELDS}
    sources = dict(value["sources"])
    if result["concern"] is not None and result["concern"] not in ("HYDRATION", "CLEANSING"):
        raise ValueError("Unsupported product need")
    budget = result["budget"]
    if budget is not None and (type(budget) not in (int, float) or not math.isfinite(budget)
                               or not 0 < budget <= 10000 or round(budget, 2) != budget):
        raise ValueError("Invalid AUD budget")
    if result["fragranceFree"] is not None and type(result["fragranceFree"]) is not bool:
        raise ValueError("Invalid fragrance preference")
    for key in FIELDS:
        quote = sources[key]
        if result[key] is None:
            if quote is not None:
                raise ValueError("Source without a value")
        elif (not isinstance(quote, str) or not quote.strip() or len(quote) > 600
              or not any(quote in text for text in messages)):
            raise ValueError("Missing literal Customer source")
    if budget is not None:
        quote = sources["budget"]
        if (not re.search(r"\$|\bbudget\b|\baud\b|澳元|澳币|预算", quote, re.I)
                or re.search(r"\busd\b|\beur\b|\bgbp\b|美元|欧元|英镑", quote, re.I)):
            raise ValueError("No explicit AUD budget source")
        amounts = re.findall(r"(?<![\d.])\d+(?:\.\d{1,2})?(?!\d|\.\d)", quote)
        if not any(float(amount) == budget for amount in amounts):
            raise ValueError("Budget is not in the quoted source")
    if result["fragranceFree"] is not None and not re.search(
            r"fragrance|scent|perfum|无香|香精|香味|香水", sources["fragranceFree"], re.I):
        raise ValueError("No explicit fragrance source")
    return {**result, "sources": sources}


def mock_extract(messages):
    """Small English/Chinese fixture grammar, visibly mock, never general NLP."""
    values = dict.fromkeys(FIELDS)
    sources = dict.fromkeys(FIELDS)
    for text in messages:
        hydration = re.search(r"hydrat\w*|dry skin|moisturi\w*|保湿|干燥|干皮", text, re.I)
        cleansing = re.search(r"cleans\w*|face wash|洁面|清洁", text, re.I)
        if hydration or cleansing:
            values["concern"] = None if hydration and cleansing else "HYDRATION" if hydration else "CLEANSING"
            sources["concern"] = (hydration or cleansing)[0] if values["concern"] else None
        amounts = list(re.finditer(r"(?:\$|AUD\s*|budget\s*(?:of|is|:)?\s*|预算\s*)(\d+(?:\.\d{1,2})?)(?!\d|\.\d)", text, re.I))
        if not amounts:
            amounts = list(re.finditer(r"(?<![\d.])(\d+(?:\.\d{1,2})?)\s*(?:AUD\b|澳元|澳币)", text, re.I))
        if amounts:
            unambiguous = len({float(amount[1]) for amount in amounts}) == 1
            values["budget"] = float(amounts[0][1]) if unambiguous else None
            sources["budget"] = amounts[0][0] if unambiguous else None
        optional = re.search(r"fragrance (?:is )?(?:fine|okay|ok)|scent (?:is )?(?:fine|okay)|不要求无香|有香.*可以|香味无所谓", text, re.I)
        required = re.search(r"fragrance[ -]free|unscented|无香|不含香精|不要香精", text, re.I)
        if optional:
            values["fragranceFree"] = False; sources["fragranceFree"] = optional[0]
        elif required:
            values["fragranceFree"] = True; sources["fragranceFree"] = required[0]
    return validate_extraction({**values, "sources": sources}, messages)
