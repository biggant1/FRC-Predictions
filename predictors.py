import tba
from typing import Callable
from typing import Any

def predict_alliances_by_rank(ranking: list[tba.Team]) -> list[tba.Alliance]:
    """Assume each team always picks the highest ranked team available"""
    alliances = []

    back_index = 23
    for i in range(0, 15, 2):
        alliances.append(tba.Alliance(ranking[i], ranking[i+1], ranking[back_index], i // 2 + 1))
        back_index -= 1
    return alliances

def calculate_alliance_error(actual: list[tba.Alliance], expected: list[tba.Alliance]):
    """Calculates the mean absolute error between the predicted rankings of alliance members and the actual rankings"""

    errors = []
    for actual_alliance, expected_alliance in zip(actual, expected):
        expected_teams = [ expected_alliance.captain, expected_alliance.first_pick, expected_alliance.second_pick ]
        actual_teams = [ actual_alliance.captain, actual_alliance.first_pick, actual_alliance.second_pick ]

        error = 0
        for expected_team, actual_team in zip(expected_teams, actual_teams):
            error += abs(actual_team.ranking - expected_team.ranking)
        errors.append(error / 3)
    return sum(errors) / len(errors)

def predict_winning_alliance(alliances: list[tba.Alliance], comparator: Callable[[tba.Alliance], int]) -> tba.Alliance:
    """Predict the winner based on a comparator function's output (lower is better)"""
    alliances.sort(key=comparator)
    return alliances[0]

def by_alliance_number(alliance: tba.Alliance) -> int:
    return alliance.alliance_number

def by_total_rankings(alliance: tba.Alliance) -> int:
    return alliance.captain.ranking + alliance.first_pick.ranking + alliance.second_pick.ranking

def by_partial_rankings(alliance: tba.Alliance) -> int:
    return alliance.captain.ranking + alliance.first_pick.ranking

def get_playoffs_distance(status: str, double_elim_round: str) -> int:
    if status == "won":
        return 7
    if double_elim_round == "Finals":
        return 6
    return int(double_elim_round[-1])

def get_playoffs_wins(status: dict[str, Any]) -> int:
    return status["record"]["wins"]