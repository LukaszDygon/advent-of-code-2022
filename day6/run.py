from aoc_helpers import input_helper


def main():
    sig = input_helper.get_lines(6)[0]
    print("1:", get_marker(sig, 4))
    print("2:", get_marker(sig, 14))

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