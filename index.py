import tba
from tqdm import tqdm
from predictors import *

def main():
    results = []
    events = tba.read_events_from_file("events.csv")

    for event in events:
        try:
            alliances = tba.get_event_alliances(event)
            predicted_winner = predict_winning_alliance(alliances, by_partial_rankings)
            actual_winner = tba.get_winning_alliance(event)
            if predicted_winner == actual_winner:
                results.append(1)
            else:
                results.append(0)
        except Exception as e:
            print("failed", event)

    print(f"Accuracy: {sum(results) / len(results)}")

if __name__ == "__main__":
    main()