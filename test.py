from datetime import datetime
from pprint import pprint

from lib.new_parser import parse

if __name__ == '__main__':
    pprint(parse("8В92", datetime.now())[2][1])