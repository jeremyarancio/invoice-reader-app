import pytest


def assert_status_code(response, expected_status):
    """
    Assert that the response has the expected status code.
    If not, raise an error with the response body for better debugging.
    """
    if response.status_code != expected_status:
        error_msg = (
            f"Expected status code {expected_status}, got {response.status_code}"
        )
        try:
            error_msg += f"\nResponse body: {response.json()}"
        except:
            error_msg += f"\nResponse text: {response.text}"
        pytest.fail(error_msg)
