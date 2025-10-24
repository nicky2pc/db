import pytest
from run import solve



EXAMPLE1 = [
    "#############",
    "#...........#",
    "###B#C#B#D###",
    "  #A#D#C#A#",
    "  #########"
]

EXAMPLE2 = [
    "#############",
    "#...........#",
    "###B#C#B#D###",
    "  #D#C#B#A#",
    "  #D#B#A#C#",
    "  #A#D#C#A#",
    "  #########"
]


def test_example1():
    assert solve(EXAMPLE1) == 12521


def test_example2():
    assert solve(EXAMPLE2) == 44169


def test_already_solved():
    solved = [
        "#############",
        "#...........#",
        "###A#B#C#D###",
        "  #A#B#C#D#",
        "  #########"
    ]
    assert solve(solved) == 0