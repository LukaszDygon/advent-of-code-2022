import os
import requests
from  datetime import datetime

AOC_SESSION = "53616c7465645f5f81977915b5c5753d5aa5e5b698bc03c3c778f83b5cf7437bfdaccaec69556d583ede178a92f39b19b01a081ce832e9a6cb74baab59cf5ede"
EMAIL = "godsofforgiveness@gmail.com"

def init_day(day):
    aoc_url = f"https://adventofcode.com/2022/day/{day}/input"
    os.mkdir(f"day{day}")
    with open(f"day{day}/input.txt", "w") as f:
        f.write(requests.get(aoc_url, cookies={"session": AOC_SESSION}, headers={"User-Agent": EMAIL}).text)

if __name__ == '__main__':
    day = datetime.now().day
    init_day(day)