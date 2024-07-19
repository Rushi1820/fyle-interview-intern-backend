import pytest
from core.libs.exceptions import FyleError
from core.libs.assertions import base_assert, assert_auth, assert_true, assert_valid, assert_found

def test_base_assert():
    # This test should raise an error to validate that base_assert behaves as expected.
    with pytest.raises(FyleError) as excinfo:
        base_assert(400, 'Custom Error Message')
    
    assert excinfo.value.status_code == 400
    assert excinfo.value.message == 'Custom Error Message'

def test_assert_auth_failure():
    # This test checks that assert_auth raises FyleError when the condition is False
    with pytest.raises(FyleError) as excinfo:
        assert_auth(False)
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.message == 'UNAUTHORIZED'

def test_assert_auth_success():
    # This test ensures no exception is raised when the condition is True
    try:
        assert_auth(True)
    except FyleError:
        pytest.fail("assert_auth raised FyleError unexpectedly!")

def test_assert_true_failure():
    # This test checks that assert_true raises FyleError when the condition is False
    with pytest.raises(FyleError) as excinfo:
        assert_true(False)
    
    assert excinfo.value.status_code == 403
    assert excinfo.value.message == 'FORBIDDEN'

def test_assert_true_success():
    # This test ensures no exception is raised when the condition is True
    try:
        assert_true(True)
    except FyleError:
        pytest.fail("assert_true raised FyleError unexpectedly!")

def test_assert_valid_failure():
    # This test checks that assert_valid raises FyleError when the condition is False
    with pytest.raises(FyleError) as excinfo:
        assert_valid(False)
    
    assert excinfo.value.status_code == 400
    assert excinfo.value.message == 'BAD_REQUEST'

def test_assert_valid_success():
    # This test ensures no exception is raised when the condition is True
    try:
        assert_valid(True)
    except FyleError:
        pytest.fail("assert_valid raised FyleError unexpectedly!")

def test_assert_found_failure():
    # This test checks that assert_found raises FyleError when the object is None
    with pytest.raises(FyleError) as excinfo:
        assert_found(None)
    
    assert excinfo.value.status_code == 404
    assert excinfo.value.message == 'NOT_FOUND'

def test_assert_found_success():
    # This test ensures no exception is raised when the object is not None
    try:
        assert_found(object())
    except FyleError:
        pytest.fail("assert_found raised FyleError unexpectedly!")
