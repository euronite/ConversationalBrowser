import pytest
from conversationalbrowser import data_manipulation as dm
import pandas as pd
import numpy as np


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
            "end",
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
            "receiver_M",
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
    assert dm.total_overlap_occurrence(test_data) == 2


def test_total_overlap_time(test_data):
    assert pytest.approx(dm.total_overlap_time(test_data)) == 1.25


def test_mean_overlap_time(test_data):
    assert pytest.approx(dm.mean_overlap_time(test_data)) == 0.625


def test_individual_call_length(test_data):
    expected = {"F01": 4.2, "F02": 2.1}
    assert expected == dm.individual_call_length(test_data)


def test_mean_call_length(test_data):
    assert pytest.approx(dm.mean_call_length(test_data)) == 3.15


def test_get_call_df(test_data):
    rows = dm.get_call_df(test_data, "F01")
    assert (rows.shape[0] == 7) and (len(rows['call'].value_counts()) == 1)


def test_receiver_and_caller_column(test_data):
    data = {
        "call": [
            "F01",
            "F01",
            "F01",
            "F01",
            "F01",
            "F01",
            "F01",
        ],
        "conversation_topic": ["n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "end", ],
        "person_and_type": [
            "silence",
            "caller_F",
            "caller_F laughter_rM",
            "caller_F receiver_M",
            "silence",
            "receiver_M",
            "end",
        ],
        "start": [0, 1.01, 1.24, 2.0, 2.9, 3.456, 4.0],
        "end": [1.01, 1.24, 2.0, 2.9, 3.456, 4.0, 4.2],
    }
    data = pd.DataFrame(data)
    data["caller"] = np.nan
    data["receiver"] = np.nan
    data = dm.receiver_and_caller_column(data)
    caller = data.caller.unique()
    receiver = data.receiver.unique()
    assert len(caller) == 1 and caller[0] == "caller_F"
    assert len(receiver) == 1 and receiver[0] == "receiver_M"
