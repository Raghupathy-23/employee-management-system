from app.utils.pagination import paginate


def test_paginate_first_page():
    result = paginate([1, 2], total=5, skip=0, limit=2)
    assert result == {
        "items": [1, 2],
        "total": 5,
        "skip": 0,
        "limit": 2,
        "has_next": True,
        "has_previous": False,
    }


def test_paginate_middle_page():
    result = paginate([3, 4], total=5, skip=2, limit=2)
    assert result["has_next"] is True
    assert result["has_previous"] is True
