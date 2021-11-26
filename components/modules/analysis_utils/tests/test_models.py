from analysis_utils.models import DataPoint
import pytest
from pydantic.error_wrappers import ValidationError

from .fixtures import default_data_point_vals


def test_data_point(default_data_point_vals):
    data_point = DataPoint(measurement=default_data_point_vals['measurement'],
                           time=default_data_point_vals['time'],
                           tags=default_data_point_vals['tags'],
                           fields=default_data_point_vals['fields'])
    data_point_dict = data_point.dict(by_alias=True)

    assert data_point_dict['measurement'] == data_point.measurement == default_data_point_vals['measurement']
    assert data_point_dict['time'] == data_point.time == default_data_point_vals['time']
    assert data_point_dict['tags'] == data_point.tags == default_data_point_vals['tags']
    assert data_point_dict['fields'] == data_point.fields_value == default_data_point_vals['fields']


def test_data_point_no_time(default_data_point_vals):
    with pytest.raises(ValidationError):
        assert DataPoint(measurement=default_data_point_vals['measurement'],
                         tags=default_data_point_vals['tags'],
                         fields=default_data_point_vals['fields'])


def test_data_point_no_measurement(default_data_point_vals):
    with pytest.raises(ValidationError):
        assert DataPoint(time=default_data_point_vals['time'],
                         tags=default_data_point_vals['tags'],
                         fields=default_data_point_vals['fields'])


def test_data_point_no_tags(default_data_point_vals):
    with pytest.raises(ValidationError):
        assert DataPoint(measurement=default_data_point_vals['measurement'],
                         time=default_data_point_vals['time'],
                         fields=default_data_point_vals['fields'])


def test_data_point_no_fields(default_data_point_vals):
    with pytest.raises(ValidationError):
        assert DataPoint(measurement=default_data_point_vals['measurement'],
                         time=default_data_point_vals['time'],
                         tags=default_data_point_vals['tags'])
