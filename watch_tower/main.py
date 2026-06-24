import argparse
import json
from pydantic import BaseModel, Field, ValidationError
from datetime import date, datetime



class Holding(BaseModel):
    ticker: str
    notes: str
    added_date: datetime = Field(default_factory=datetime.now)

def stock_parser():
    """
    A class that does parsing for the terminal command
    And helps in saving tickers with notes
    And also lists them for you 
    """

    try:
        data = read_json()
        for entry in data.values():
            Holding.model_validate(entry)
    except FileNotFoundError:
        print("There is no data, initiating a new dict")
        data = {}
    except ValidationError as e:
        print(f"You have a bad entry: {e}")
        return

    parser = argparse.ArgumentParser(
        prog="TickerSaver",
        description="Saves stocks tickers with notes",
        epilog="Thanks for using TickerSaver!"
    )

    parser.add_argument('-a', '--add', nargs=2, help="it adds a ticker to the file")
    parser.add_argument('-l', '--list', action = "store_true" ,help="a function that lists all existing tickers")

    args = parser.parse_args()

    if args.add:
        ticker, note = args.add
        if ticker in data.keys():
            print("The ticker already has a note, overriding the current one")
        holding = Holding(ticker=ticker, notes=note)
        data[ticker] = holding.model_dump(mode="json")
        write_json(data)

    if args.list:
            print("Here is the data:")
            for key in data.keys():
                print(f"{key}: {data[key]}")
        

def read_json():
    with open(file='data.json', mode='r', encoding='utf-8') as f:
        return json.load(f)

def write_json(data : dict):
    with open(file='data.json', mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent = 4)


if __name__ == "__main__":
    stock_parser()
