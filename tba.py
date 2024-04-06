import requests
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Any
load_dotenv()

TBA_BASE_PATH = "https://www.thebluealliance.com/api/v3"
HEADERS = { "X-TBA-Auth-Key": os.environ['TBA_KEY'] }

@dataclass
class Team:
    """Holds all the relevant information about a team at a specific event"""
    team_key: str
    event_key: str
    ranking: int

@dataclass
class Alliance:
    captain: Team
    first_pick: Team
    second_pick: Team
    alliance_number: int

def request(path: str):
    response = requests.get(f"{TBA_BASE_PATH}{path}", headers=HEADERS)
    data = response.json()
    if "Error" in data:
        raise Exception(data['Error'])
    return data

def write_events(*, year: str, filename: str) -> None:
    events = request(f"/events/{year}")
    output = []
    for event in events:
        if event["event_type_string"] != "Regional": continue

        output.append(event['key'])

    with open(filename, 'w') as f:
        f.write("\n".join(output))

def read_events_from_file(filename: str) -> None:
    with open(filename) as f:
        return f.read().splitlines()
    
def get_event_rankings(event_key: str) -> list[Team]:
    data = request(f"/event/{event_key}/rankings")
    rankings = [Team(team_key=ranking["team_key"], event_key=event_key, ranking=i+1) 
                    for i, ranking in enumerate(data["rankings"])]
    return rankings

def __team_key_to_team_map(event_key: str):
    rankings = get_event_rankings(event_key)
    team_key_to_team = {}
    for ranking in rankings:
        team_key_to_team[ranking.team_key] = ranking
    return team_key_to_team

def get_event_alliances(event_key: str) -> list[Alliance]:
    data = request(f"/event/{event_key}/alliances")
    team_key_to_team = __team_key_to_team_map(event_key)
    alliances = []
    for i, alliance in enumerate(data):
        picks = alliance["picks"]
        alliances.append(Alliance(team_key_to_team[picks[0]], team_key_to_team[picks[1]], team_key_to_team[picks[2]], i+1))
    return alliances

def get_event_alliances_with_extra_data(event_key: str) -> list[tuple[dict[str, Any], Alliance]]:
    """Returns status, alliance"""
    data = request(f"/event/{event_key}/alliances")
    team_key_to_team = __team_key_to_team_map(event_key)
    alliances = []
    for i, alliance in enumerate(data):
        picks = alliance["picks"]
        alliances.append((alliance["status"], 
                          Alliance(team_key_to_team[picks[0]], 
                                   team_key_to_team[picks[1]], team_key_to_team[picks[2]], i+1)))
    return alliances

def get_winning_alliance(event_key: str) -> Alliance:
    alliances_with_results = get_event_alliances_with_extra_data(event_key)
    for status, alliance in alliances_with_results:
        if status["status"] == "won":
            return alliance