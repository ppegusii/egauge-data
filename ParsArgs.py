import argparse
import json
import sys


'''
This script is an example of how to parse arguments in python.
Examples of how to run the program:
    ./argparse_example.py label -l label_list.json
    ./argparse_example.py egauge
    ./argparse_example.py -h
'''


def main():
    args = parseArgs(sys.argv)
    print args


def parseArgs(args):
    parser = argparse.ArgumentParser(
        description='Description of the eGauge-data program.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('sort',
                        type=sortType,
                        help='Sort by "eGauge" or "label".')
    parser.add_argument('-l', '--labellist',
                        type=jsonList,
                        help='Optional list of labels in JSON format.')
    return parser.parse_args()


def sortType(s):
    s = s.lower()
    assert (s == 'egauge' or s == 'label')
    return s


def jsonList(fileName):
    with open(fileName, 'rU') as f:
        l = json.load(f)
    assert type(l) == list
    return l

if __name__ == '__main__':
    main()