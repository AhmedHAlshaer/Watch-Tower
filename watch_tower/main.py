import argparse
import json


def stocks_parser():
    try:
        data = read_json()
    except Exception as e:
        print(f"There is no data due to: {e}, initiating a new dict")
        data = {}

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
            data[ticker] = note
        else:
            data[ticker] = note
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
    stocks_parser()
