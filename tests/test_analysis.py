import pytest
from conversationalbrowser import data_manipulation as dm
import pandas as pd
import numpy as np
from pathlib import Path


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
    return pd.DataFrame(data)


@pytest.fixture
def individual_call_data_2():
    dummy_data = {
        "call": ["F01", "F01", "F01", "F01", "F01", "F01"],
        "conversation_topic": [
            "other",
            "other",
            "other",
            "other",
            "other",
            "end",
        ],
        "person_and_type": [
            "silence",
            "filler_cM filler_rF",
            "laughter_cM",
            "laughter_rF",
            "laughter_cM",
            "end",
        ],
        "start": [
            0,
            1.01,
            1.24,
            2.0,
            2.9,
            3.456,
        ],
        "end": [
            1.01,
            1.24,
            2.0,
            2.9,
            3.456,
            4.0,
        ],
        "caller": [
            "caller_M",
            "caller_M",
            "caller_M",
            "caller_M",
            "caller_M",
            "caller_M",
        ],
        "receiver": [
            "receiver_F",
            "receiver_F",
            "receiver_F",
            "receiver_F",
            "receiver_F",
            "receiver_F",
        ],
    }
    return pd.DataFrame(dummy_data)


@pytest.fixture
def individual_call_data():
    dummy_data = {
        "call": ["F01", "F01", "F01", "F01", "F01", "F01"],
        "conversation_topic": [
            "other",
            "other",
            "other",
            "other",
            "other",
            "end",
        ],
        "person_and_type": [
            "silence",
            "caller_F",
            "laughter_cF",
            "laughter_rM",
            "laughter_cF",
            "end",
        ],
        "start": [
            0,
            1.01,
            1.24,
            2.0,
            2.9,
            3.456,
        ],
        "end": [
            1.01,
            1.24,
            2.0,
            2.9,
            3.456,
            4.0,
        ],
        "caller": [
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
        ],
    }
    return pd.DataFrame(dummy_data)


def test_get_non_verbal_speech(test_data):
    assert len(dm.get_non_verbal_speech_only(test_data, "silence")) == 3
    assert len(dm.get_non_verbal_speech_only(test_data, "laughter_cF")) == 0


def test_read_in():
    assert dm.read_in_data(Path("tests/test_data.csv")) is not None


def test_occurrence_of_event(individual_call_data, individual_call_data_2):
    assert [2, 1] == dm.occurrence_of_event(individual_call_data, "laughter")
    assert [1, 1] == dm.occurrence_of_event(individual_call_data, "silence")
    with pytest.raises(ValueError):
        dm.occurrence_of_event(pd.DataFrame(), "laughter")

    assert [2, 1] == dm.occurrence_of_event(individual_call_data_2, "laughter")
    assert [1, 1] == dm.occurrence_of_event(individual_call_data_2, "silence")


def test_get_list_of_call_id_df(test_data):
    assert len(dm.get_list_of_call_id_df(test_data, ["F01", "F02"])) == 11


def test_total_time_of_event(individual_call_data, individual_call_data_2):
    assert pytest.approx([1.316, 0.9]) == dm.total_time_of_event(
        individual_call_data, "laughter"
    )
    assert pytest.approx([1.316, 0.9]) == dm.total_time_of_event(
        individual_call_data_2, "laughter"
    )
    with pytest.raises(ValueError):
        dm.total_time_of_event(pd.DataFrame(), "laughter")


def test_get_permutations_of_gender_and_position():
    expected = [
        "caller_F receiver_M",
        "caller_F receiver_F",
        "caller_M receiver_M",
        "caller_M receiver_F",
    ]
    assert any(
        elem in dm.get_permutations_of_gender_and_position() for elem in expected
    )


def test_get_rows_by_caller_and_receiver(test_data):
    df = dm.get_rows_by_caller_and_receiver(test_data, "caller_F", "receiver_F")
    assert "caller_F" in df.caller.unique() and len(df.caller.unique()) == 1
    assert "receiver_F" in df.receiver.unique() and len(df.receiver.unique()) == 1
    df = dm.get_rows_by_caller_and_receiver(test_data, "caller_F", "receiver_M")
    assert "caller_F" in df.caller.unique() and len(df.caller.unique()) == 1
    assert "receiver_M" in df.receiver.unique() and len(df.receiver.unique()) == 1
    df = dm.get_rows_by_caller_and_receiver(test_data, None, None)
    assert len(df.caller.unique()) == 1
    assert len(df.receiver.unique()) == 2


def test_get_rows_by_caller_and_receiver_with_missing_pos(test_data):
    df = dm.get_rows_by_caller_and_receiver(test_data, "caller_F", None)
    assert "caller_F" in df.caller.unique() and len(df.caller.unique()) == 1
    df = dm.get_rows_by_caller_and_receiver(test_data, None, "receiver_F")
    assert "receiver_F" in df.receiver.unique() and len(df.receiver.unique()) == 1


def test_occurrence_of_each_event(test_data, individual_call_data_2):
    result = dm.occurrence_of_each_event(test_data, dm.cue_types)
    assert pytest.approx(result["silence"]) == 3
    assert pytest.approx(result["laughter"]) == 1
    assert result["filler"] == 0
    assert result["bc"] == 0
    assert (
        dm.occurrence_of_each_event(individual_call_data_2, dm.cue_types)["filler"] == 2
    )


def test_mean_time_of_each_event(test_data):
    result = dm.mean_time_of_each_event(test_data, dm.cue_types)
    assert pytest.approx(result["silence"]) == 0.705333333
    assert pytest.approx(result["laughter"]) == 0.76
    assert result["filler"] == 2
    assert result["bc"] == 0


def test_total_time_of_each_event(test_data):
    result = dm.total_time_of_each_event(test_data, dm.cue_types)
    assert pytest.approx(result["silence"]) == 2.116
    assert pytest.approx(result["laughter"]) == 0.76
    assert result["filler"] == 0
    assert result["bc"] == 0


def test_get_all_event_durations(test_data):
    result = dm.get_all_event_durations(test_data, "laughter")
    assert len(result[0]) == 0 and result[1].iloc[0] == 0.76
    result = dm.get_all_event_durations(test_data, "silence")
    assert len(result[0]) == 3 and result[1].iloc[0] == 1.01


def test_get_all_event_durations_raised_error(test_data):
    with pytest.raises(ValueError):
        dm.get_all_event_durations(pd.DataFrame({"A": []}), "silence")


def test_get_all_call_ids(test_data):
    assert len((dm.get_all_call_ids(test_data))) == 2


def test_get_call_df(test_data):
    rows = dm.get_call_df(test_data, "F01")
    assert (rows.shape[0] == 7) and (len(rows["call"].value_counts()) == 1)


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
        "conversation_topic": [
            "n/a",
            "n/a",
            "n/a",
            "n/a",
            "n/a",
            "n/a",
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
