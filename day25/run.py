from aoc_helpers import input_helper


def main():
    lines = input_helper.get_lines(25)
    decimal_numbers = [to_decimal(line) for line in lines]
    s = sum(decimal_numbers)
    print(s)
    print(to_decimal(to_bs_5(s)))
    print("1:", to_bs_5(sum(decimal_numbers)))
    print("2:", "")

def to_decimal(line: str) -> int:
    total = 0
    base_multiplier = 1
    for i in range(len(line)):
        i = len(line) - i - 1
        if line[i] == "2":
            total += 2 * base_multiplier
        elif line[i] == "1":
            total += base_multiplier
        elif line[i] == "-":
            total -= base_multiplier
        elif line[i] == "=":
            total -= base_multiplier * 2
        
        base_multiplier *= 5
    return total

def to_bs_5(number: int) -> str:
    digit_to_bs_5 = {0: '0', 1: '1', 2: '2', 3: '=', 4: '-'}
    bs_5 = ''
    while number > 0:
        number, rem = divmod(number, 5)
        bs_5 += digit_to_bs_5[rem]
        if rem > 2:
            number += 1
    return bs_5[::-1] if bs_5 else '0'
if __name__ == "__main__":
    main()