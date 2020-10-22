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


def test_get_permutations_of_gender_and_position():
    expected = ['caller_F receiver_M', 'caller_F receiver_F', 'caller_M receiver_M', 'caller_M receiver_F']
    assert any(elem in dm.get_permutations_of_gender_and_position() for elem in expected)


def test_get_rows_by_caller_and_receiver(test_data):
    df = dm.get_rows_by_caller_and_receiver(test_data, "caller_F", "receiver_F")
    assert "caller_F" in df.caller.unique() and len(df.caller.unique()) == 1
    assert "receiver_F" in df.receiver.unique() and len(df.receiver.unique()) == 1


def test_occurrence_of_each_event(test_data):
    result = dm.occurrence_of_each_event(test_data, dm.cue_types)
    assert pytest.approx(result["silence"]) == 3
    assert pytest.approx(result["laughter"]) == 1
    assert result["filler"] == 0
    assert result["bc"] == 0

def test_mean_time_of_each_event(test_data):
    result = dm.mean_time_of_each_event(test_data, dm.cue_types)
    assert pytest.approx(result["silence"]) == 0.705333333
    assert pytest.approx(result["laughter"]) == 0.76
    assert result["filler"] == 0
    assert result["bc"] == 0


def test_total_time_of_each_event(test_data):
    result = dm.total_time_of_each_event(test_data, dm.cue_types)
    assert pytest.approx(result["silence"]) == 2.116
    assert pytest.approx(result["laughter"]) == 0.76
    assert result["filler"] == 0
    assert result["bc"] == 0


def test_remove_conversation_topic_df(test_data):
    df = dm.remove_conversation_topic_df(test_data, "other")
    assert "other" not in df.conversation_topic.unique()


def test_get_conversation_only_df(test_data):
    df = dm.get_conversation_only_df(test_data, dm.cue_types.keys())
    assert not any(elem in df["person_and_type"].tolist() for elem in dm.cue_types.keys())


def test_get_conversation_topic_df(test_data):
    df = dm.get_conversation_topic_df(test_data, "end")
    assert "other" not in df.conversation_topic.unique()


def test_convert_to_minutes_and_seconds():
    assert str(dm.convert_to_minutes_and_seconds(10000)) == "2:46:40"


def test_get_all_conversation_topics(test_data):
    assert len(dm.get_all_conversation_topics(test_data)) == 2


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


def test_get_all_call_ids(test_data):
    assert len((dm.get_all_call_ids(test_data))) == 2


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
