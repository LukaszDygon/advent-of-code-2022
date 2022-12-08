from aoc_helpers import input_helper


def main():
    lines = input_helper.get_lines(6)[0]
    print([[int(a) for a in range(i, len(lines)) if len(set(lines[int(a)-i:int(a)])) == i][0] for i in [4, 14]])

    print("1:", get_marker(lines, 4))
    print("2:", get_marker(lines, 14))
    

def get_marker(sig: str, marker_length: int = 4) -> int:
    i = 1
    unique = sig[0]
    while len(unique) != marker_length:
        j = len(unique) - 1
        while j != -1:
            if unique[j] == sig[i]:
                break
            j -= 1
        unique = unique[j+1:] + sig[i]
        i += 1
    return i

if __name__ == "__main__":
    main()