import conversationalbrowser.graph as graph
import pytest
from matplotlib.figure import Figure


# test unit tests run and are able to pass
def test_assert():
    test_value = 1
    assert test_value == 1


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
