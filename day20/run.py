from typing import List
from aoc_helpers import input_helper
from collections import deque


def mixing(lines: List[str], key: int=1, n_times: int=1) -> List[int]:
    dq = deque(enumerate((int(line) * key for line in lines)))
    for _ in range(n_times):
        for idx in range(len(dq)):
            while dq[0][0] != idx:
                dq.rotate(-1)

            ord_n, shift_n = dq.popleft()
            dq.rotate(-1 * shift_n)
            dq.appendleft((ord_n, shift_n))

    return dq


def find_coord(data):  # cba arithmetics
    while data[0][1] != 0:
        data.rotate(-1)

    coord = list()
    for _ in range(3):
        for _ in range(1000):
            data.rotate(-1)
        coord.append(data[0][1])
    return sum(coord)

def main():
    lines = input_helper.get_lines(20)

    print("1:", find_coord(mixing(lines)))
    print("2:", find_coord(mixing(lines, 811589153, 10)))

if __name__ == "__main__":
    main()