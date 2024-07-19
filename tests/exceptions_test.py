import pytest
from core.libs.exceptions import FyleError

def test_fyle_error_instantiation():
    error = FyleError(status_code=418, message="This is a FyleError")
    assert error.status_code == 418
    assert error.message == "This is a FyleError"

def test_fyle_error_to_dict():
    error = FyleError(status_code=418, message="This is a FyleError")
    error_dict = error.to_dict()
    assert error_dict == {"message": "This is a FyleError"}

def test_fyle_error_raises():
    with pytest.raises(FyleError) as excinfo:
        raise FyleError(status_code=418, message="This is a FyleError")
    assert excinfo.value.status_code == 418
    assert excinfo.value.message == "This is a FyleError"
