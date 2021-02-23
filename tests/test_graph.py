import conversationalbrowser.graph as graph
import pytest
from matplotlib.figure import Figure
from conversationalbrowser.model import CallerModel
import pandas as pd
import main

# test unit tests run and are able to pass
def test_assert():
    test_value = 1
    assert test_value == 1


def test_get_df(qtbot, main_window, caller_model, test_data):
    qtbot.addWidget(main_window)
    caller_model.set_selected_items(["F01", "F02"])
    caller_model.cues_selected = [("laughter", 0)]
    df, cue_types = graph.get_df(main_window, caller_model, test_data)
    assert df.empty
    assert cue_types == {"laughter": 0}


def test_set_labels(ax):
    graph.set_label(ax, "Callers", "occurrences", False)
    assert ax.title.get_text() == "Total Cue Occurrences for Callers"
    assert ax.get_ylabel() == "Total Number of Occurrences"
    assert ax.get_xlabel() == "Cue"
    graph.set_label(ax, "Callers", "occurrences", True)
    assert ax.title.get_text() == "Average Total Cue Occurrences for Callers Per Call"
    assert ax.get_ylabel() == "Average Total Number of Occurrences"
    graph.set_label(ax, "Callers", "durations", False)
    assert ax.title.get_text() == "Total Cue Duration for Callers"
    assert ax.get_ylabel() == "Total Duration (s)"


@pytest.fixture
def ax():
    fig = Figure()
    ax = fig.add_subplot(111)
    return ax


@pytest.fixture
def main_window():
    return main.MainWindow()


@pytest.fixture
def test_data():
    data = {
        "call": [
            "F01",
            "F01",
            "F02",
            "F02",
        ],
        "conversation_topic": [
            "other",
            "end",
            "other",
            "end",
        ],
        "person_and_type": [
            "laughter_cF",
            "end",
            "caller_F receiver_F",
            "end",
        ],
        "start": [0, 4.0, 0, 2.0],
        "end": [1.01, 4.2, 1.1, 2.1],
        "caller": [
            "caller_F",
            "caller_F",
            "caller_F",
            "caller_F",
        ],
        "receiver": [
            "receiver_M",
            "receiver_M",
            "receiver_F",
            "receiver_F",
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture
def caller_model():
    return CallerModel()
