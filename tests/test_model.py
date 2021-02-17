from conversationalbrowser import model
import pytest
import pandas as pd


# test unit tests run and are able to pass
def test_assert():
    test_value = 1
    assert test_value == 1


def test_is_valid_error():
    assert model.is_valid("test.file") is False


def test_is_valid():
    model.is_valid("main.py")


def test_set_file_name(test_data_model):
    test_data_model.set_file_name("error.csv")
    assert test_data_model.fileName == ""


def test_set_selected_items(test_call_model):
    test_call_model.set_selected_items(["F01", "F02"])
    assert test_call_model.selected == ["F01", "F02"]


def test_set_caller_ids(test_data_model):
    test_data_model.set_caller_ids(["F01", "F02", "F03"])
    assert test_data_model.callerIds == ["F01", "F02", "F03"]


def test_set_figure(test_data_model):
    test_data_model.set_figure("TEST FIGURE")
    assert test_data_model.figure == "TEST FIGURE"


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
