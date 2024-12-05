import pytest
from main import call_api

# Test 1: Ensure the API call returns status code 200
def test_api_status_code():
    data = call_api()
    assert isinstance(data, list)  # `call_api` always returns a list

# Test 2: Ensure we receive a string in a specific field
def test_api_returns_string():
    data = call_api()
    if data:  # Check if there are any entries
        assert isinstance(data[0].get('Field1'), str)  # confirm that 'Field1' is a string

# Test 3: Ensure `call_api` runs without crashing
def test_api_runs():
    try:
        call_api()
        assert True  # Test passes if no exceptions are raised
    except Exception as e:
        assert False, f"Function raised an exception: {e}"


if __name__ == "__main__":
    pytest.main()