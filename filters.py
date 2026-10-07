def filter_location(location: str) -> tuple[bool, str]:
    location_lower = location.lower()

    if "except new york" in location_lower:
        return False, "Location not eligible"

    if "new york" in location_lower:
        return True, "New York"

    if "remote" in location_lower and "us" in location_lower:
        return True, "US remote"

    return False, "Location not eligible"