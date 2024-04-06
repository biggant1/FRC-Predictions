import tba
from tqdm import tqdm
from predictors import *
import numpy as np

def main():
    events = tba.read_events_from_file("events.csv")

    wins = []
    alliance_numbers = []
    for event in events:
        alliances = tba.get_event_alliances_with_extra_data(event)
        for status, alliance in alliances:
            wins.append(get_playoffs_wins(status))
            alliance_numbers.append(alliance.alliance_number)

    r = np.corrcoef(wins, alliance_numbers)[0][1]
    r_square = r ** 2 
    print(f"{r=} {r_square=}")

if __name__ == "__main__":
    main()