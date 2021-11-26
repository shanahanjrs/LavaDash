import pytest


@pytest.fixture
def headline_vals():
    return {"type": "news", "data": {}, "date_time": None, "term": "military"}


@pytest.fixture
def default_data_point_vals():
    return {
        "measurement": "test_event",
        "time": "2000-11-10T23:00:00Z",
        "tags": {
            "type": "twitter"
        },
        "fields": {
            "language": "en",
            "subjectivity": "0.3",
            "polarity": "0.45",
            "author": "JohnIsSuperCool",
            "title": "My Name is Flynn and John is Cool"
        }
    }
