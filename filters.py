def filter_location(location: str) -> tuple[bool, str]:
    location_lower = location.lower()

    if "except new york" in location_lower:
        return False, "Location not eligible"

    if "new york" in location_lower:
        return True, "New York"

    if "remote" in location_lower and "us" in location_lower:
        return True, "US remote"

    if "north america" in location_lower:
        return True, "North America - preliminary"

    return False, "Location not eligible"


TITLE_GROUP_A = (
    "solutions",
    "technical",
    "account",
    "strategic",
    "customer",
    "success",
    "delivery",
    "enterprise",
    "systems",
    "integration",
    "launch",
    "partner",
    "platform",
    "client",
    "deployment",
)

TITLE_GROUP_B = (
    "architect",
    "advisor",
    "specialist",
    "manager",
    "consultant",
    "engineer",
    "lead",
    "director",
)


def filter_title(title: str) -> tuple[bool, str]:
    title_lower = title.lower()

    matches_a = any(term in title_lower for term in TITLE_GROUP_A)

    matches_b = any(term in title_lower for term in TITLE_GROUP_B)

    if matches_a and matches_b:
        return True, "Title matches both groups"

    return False, "Title does not match both groups"
