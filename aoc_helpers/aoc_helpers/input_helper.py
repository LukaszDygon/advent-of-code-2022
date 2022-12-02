def get_lines(day):
    with open(f"day{day}/input.txt") as f:
        return f.read().splitlines()