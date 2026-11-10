from filters import filter_location, filter_title


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


def test_solutions_engineer_passes():
    passed, reason = filter_title("Solutions Engineer")

    assert passed is True
    assert reason == "Title matches both groups"


def test_customer_success_manager_passes():
    passed, reason = filter_title("Customer Success Manager")

    assert passed is True


def test_product_manager_fails():
    passed, reason = filter_title("Product Manager")

    assert passed is False


def test_software_engineer_fails():
    passed, reason = filter_title("Software Engineer")

    assert passed is False


def test_title_matching_is_case_insensitive():
    passed, reason = filter_title("TECHNICAL ACCOUNT MANAGER")

    assert passed is True
