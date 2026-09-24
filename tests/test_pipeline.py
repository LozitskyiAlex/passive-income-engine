from passive_income_engine.pipeline import normalize


def test_normalize_deduplicates_and_skips_invalid_records():
    records = [
        {"id": "1", "title": "First", "url": "https://example.com/1"},
        {"id": "1", "title": "Duplicate", "url": "https://example.com/2"},
        {"id": "", "title": "Invalid", "url": "https://example.com/3"},
    ]

    items = normalize(records, "example")

    assert len(items) == 1
    assert items[0].title == "First"
    assert items[0].source == "example"
