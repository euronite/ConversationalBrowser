from conversationalbrowser import model
import pytest
import pandas as pd


# test unit tests run and are able to pass
def test_assert():
    test_value = 1
    assert test_value == 1


def test_is_valid():
    assert model.is_valid("test.file") is False


def test_get_file_contents(test_data_model):
    result = test_data_model.get_file_content()
    assert result is not None and not result.empty


def test_call_model_params(test_call_model):
    assert len(test_call_model.cues_selected) == 2
    assert test_call_model.cues_selected[0][0] == "Silence"
    assert len(test_call_model.selected) == 3


@pytest.fixture
def test_call_model():
    mod = model.CallerModel()
    mod.cues_selected = [("Silence", 1), ("Laughter", 3)]
    mod.selected = [("F01", 1), ("F02", 2), ("F03", 3)]
    return mod


@pytest.fixture
def test_data_model(test_data):
    mod = model.Model()
    mod.fileContents = pd.DataFrame(test_data)
    return mod


@pytest.fixture
def test_data():
    data = {
        "call": [
            "F01",
            "F01",
            "F01",
            "F01",
            "F01",
            "F02",
            "F02",
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
            "end",
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
            "caller_F laughter_rM",
            "caller_F receiver_M",
            "end",
            "receiver_M",
            "silence",
            "caller_F",
            "caller_F receiver_F",
            "silence",
            "end",
        ],
        "start": [0, 1.01, 1.24, 2.0, 2.9, 0, 4.0, 0, 1.1, 1.45, 2.0],
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
            "receiver_F",
            "receiver_F",
            "receiver_F",
            "receiver_F",
            "receiver_F",
            "receiver_F",
        ],
    }
    return pd.DataFrame(data)
