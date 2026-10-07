from filters import filter_location


def test_new_york_passes():
    passed, reason = filter_location("New York, NY")

    assert passed is True
    assert reason == "New York"


def test_new_york_hybrid_passes():
    passed, reason = filter_location("New York, NY (Hybrid)")

    assert passed is True
    assert reason == "New York"


def test_us_remote_passes():
    passed, reason = filter_location("Remote - US")

    assert passed is True
    assert reason == "US remote"


def test_san_francisco_fails():
    passed, reason = filter_location("San Francisco, CA")

    assert passed is False
    assert reason == "Location not eligible"


def test_remote_excluding_new_york_fails():
    passed, reason = filter_location("Remote - US except New York")

    assert passed is False
    assert reason == "Location not eligible"