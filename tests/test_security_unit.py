from app.core.security import create_access_token, is_valid_token


def test_access_token_round_trip():
    token = create_access_token("123", "ADMIN")
    assert is_valid_token(token)


def test_invalid_token_is_rejected():
    assert not is_valid_token("not-a-valid-jwt")
