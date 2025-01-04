import pandas as pd
import pytest

from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA


@pytest.fixture
def data_grabber():
    path_to_data = FAMILY_DATA
    return DataGrabber(path_to_data, sep=",")


def test_data_grabber_properties(data_grabber):
    assert data_grabber.path_to_dataset == FAMILY_DATA

    comparison = data_grabber.data_frame.compare(pd.read_csv(FAMILY_DATA, sep=","))
    assert comparison.empty


def test_data_grabber_columns(data_grabber):
    expected = [
        "family_id",
        "choice_0",
        "choice_1",
        "choice_2",
        "choice_3",
        "choice_4",
        "choice_5",
        "choice_6",
        "choice_7",
        "choice_8",
        "choice_9",
        "n_people",
    ]
    assert data_grabber.columns() == expected


@pytest.mark.parametrize(
    ("input_n", "expected"),
    [
        (0, [52, 38, 12, 82, 33, 75, 64, 76, 10, 28]),
        (1, [26, 4, 82, 5, 11, 47, 38, 6, 66, 61]),
        (16, [46, 50, 1, 17, 52, 74, 7, 21, 38, 25]),
        (44, [49, 1, 32, 45, 46, 82, 24, 60, 89, 10]),
        (100, [39, 5, 80, 1, 19, 75, 88, 94, 49, 22]),
        (6000, None),
    ],
)
def test_get_family_choices(data_grabber, input_n, expected):
    assert data_grabber.get_family_choices(input_n) == expected


@pytest.mark.parametrize(
    ("input_n", "expected"),
    [(0, 4), (1, 4), (16, 3), (44, 2), (100, 6), (6000, None)],
)
def test_get_family_size(data_grabber, input_n, expected):
    assert data_grabber.get_family_size(input_n) == expected
