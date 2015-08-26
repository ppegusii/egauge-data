import argparse
import sys
import json

def main():
    args = parseArgs(sys.argv)
    print args

def parseArgs(args):
    parser = argparse.ArgumentParser(
        description='Description of the eGauge-data program.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('eGauge_urls',
    					type=jsonList,
    					help= "A JSON list of eGauge urls to call")
    return parser.parse_args()

def jsonList(fileName):
    with open(fileName, 'r') as f:
        l = json.load(f)
    assert type(l) == list
    return l

if __name__ == '__main__':
    main()