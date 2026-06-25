import argparse
import json
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class Holding(BaseModel):
    ticker: str
    notes: str
    added_date: datetime = Field(default_factory=datetime.now)


class SchemaVersion(BaseModel):
    schema_version: int = 2
    holding: dict[str, Holding]


def migrate(raw_data) -> dict:
    if isinstance(raw_data, dict) and "schema_version" not in raw_data:
        print("💡 Legacy v1 data format detected. Migrating automatically to v2...")
        return {
            "schema_version": 2,
            "holding": raw_data
        }
    return raw_data


def stock_parser():
    """
    A class that does parsing for the terminal command
    And helps in saving tickers with notes
    And also lists them for you 
    """

    try:
        raw_data = read_json()
        data = migrate(raw_data)  
        SchemaVersion.model_validate(data)
    except FileNotFoundError:
        print("There is no data, initiating a new dict")
        data = {"schema_version": 2, "holding": {}}
    except ValidationError as e:
        print(f"You have a bad entry: {e}")
        return

    parser = argparse.ArgumentParser(
        prog="TickerSaver",
        description="Saves stocks tickers with notes",
        epilog="Thanks for using TickerSaver!"
    )

    parser.add_argument('-a', '--add', nargs=2, help="it adds a ticker to the file")
    parser.add_argument('-l', '--list', action="store_true", help="a function that lists all existing tickers")

    args = parser.parse_args()

    if args.add:
        ticker, note = args.add
        if ticker in data["holding"].keys():
            print("The ticker already has a note, overriding the current one")
            
        holding = Holding(ticker=ticker, notes=note)
        
        data["holding"][ticker] = holding.model_dump(mode="json")
        
        schema_version = SchemaVersion(schema_version=2, holding=data["holding"])
        write_json(schema_version.model_dump(mode="json"))
        print(f"Successfully saved {ticker}.")

    if args.list:
        print("Here is the data:")
        for key, value in data["holding"].items():
            print(f"{key}: {value}")
        

def read_json():
    with open(file='data.json', mode='r', encoding='utf-8') as f:
        return json.load(f)

def write_json(data: dict):
    with open(file='data.json', mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    stock_parser()