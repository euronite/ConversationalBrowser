import pytest
from conversationalbrowser import data_manipulation as dm
import pandas as pd


# test unit tests run and are able to pass
def test_assert():
    test_value = 1
    assert test_value == 1


@pytest.fixture
def test_data():
    data = {
        "call": [
            "F01",
            "F01",
            "F01",
            "F01",
            "F01",
            "F01",
            "F01",
            "F02",
            "F02",
            "F02",
            "F02",
        ],
        "conversation_topic": [
            "other",
            "other",
            "other",
            "other",
            "other",
            "other",
            "end",
            "other",
            "other",
            "other",
            "other",
        ],
        "person_and_type": [
            "silence",
            "caller_F",
            "caller_F laughter_rM",
            "caller_F receiver_M",
            "silence",
            "receiver_M",
            "end",
            "caller_F",
            "caller_F receiver_F",
            "silence",
            "end",
        ],
        "start": [0, 1.01, 1.24, 2.0, 2.9, 3.456, 4.0, 0, 1.1, 1.45, 2.0],
        "end": [1.01, 1.24, 2.0, 2.9, 3.456, 4.0, 4.2, 1.1, 1.45, 2.0, 2.1],
        "caller": [
            "caller_F",
            "caller_F",
            "caller_F",
            "caller_F",
            "caller_F",
            "caller_F",
            "caller_F",
            "caller_F",
            "caller_F",
            "caller_F",
            "caller_F",
        ],
        "receiver": [
            "receiver_M",
            "receiver   _M",
            "receiver_M",
            "receiver_M",
            "receiver_M",
            "receiver_M",
            "receiver_M",
            "receiver_F",
            "receiver_F",
            "receiver_F",
            "receiver_F",
        ],
    }
    data = pd.DataFrame(data)
    return data


def test_total_overlap_occurrence(test_data):
    assert dm.total_overlap_occurrence(test_data, dm.gender_and_position) == 2


def test_total_overlap_time(test_data):
    assert pytest.approx(dm.total_overlap_time(test_data, dm.gender_and_position)) == 1.25


def test_mean_overlap_time(test_data):
    assert pytest.approx(dm.mean_overlap_time(test_data, dm.gender_and_position)) == 0.625
