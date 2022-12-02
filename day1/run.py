from aoc_helpers import input_helper

def main():
    lines = input_helper.get_lines(1)
    individual_inventories = get_individual_inventories(lines)
    calories = sorted([sum([int(x) for x in inventory]) for inventory in individual_inventories])[::-1]
    print("1:", calories[0])
    print("2:", sum(calories[:3]))

def get_individual_inventories(lines):
    individual_inventories = []
    inventory = []
    for line in lines:
        if line == "":
            individual_inventories.append(inventory)
            inventory = []
        else:
            inventory.append(line)
    individual_inventories.append(inventory)
    return individual_inventories

if __name__ == "__main__":
    main()