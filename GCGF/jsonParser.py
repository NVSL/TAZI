import argparse
import json

parser = argparse.ArgumentParser(description="This is a test json parser")
parser.add_argument("-j", "--json", required=True)
args = parser.parse_args()


with open( args.json ) as data_file:
    data = json.load(data_file)

