Title: Advent of Code 2021 - Day 2
Date: 2021-12-02 12:30
Tags: programming, aoc, python
Summary: Advent of Code 2021 - Day 2
Slug: aoc-2021-day2
Description: Advent of Code 2021 - Day 2

**Spoiler Warning: This post contains spoilers for Advent of Code Day 2.**

Time for day 2! This one was quite simple again but still a lot of fun especially because it gave me an excuse to try out another feature of python3.10 [Structural Pattern Matching](https://www.python.org/dev/peps/pep-0636/)

### Part 1

The input for this challenge had a command per line in the format `<direction> <magnitude>` for example `down 5`. 

The task for part 1 was to calculating the resulting horizontal location and depth after all the commands had been followed then multiply them together.

First of all I defined a function to read the file and parse the input. Resulting in a list of lists where each inner list was of the format `[direction, magnitude].` Using `split` made this quite straight forward but meant I had to deal with converting the magnitude from a string to an integer later on. If anybody has any suggestions for a cleaner way to handle this please let me know.

    :::py
    def parse_input(filename: str) -> list[list[str]]:
        """Parses the file given by filename and returns a list of commands
        where each command is a list [instruction, value].
        """
        with open(filename) as f:
            planned_course = f.readlines()
        commands = [command.split() for command in planned_course]
        return commands

I'm still getting my head around type hinting so this may not be entirely correct. If somebody could let me know it would be appreciated.

Now that I have my commands it was time to follow them to get the final horizontal and depth positions.

    :::py
    def follow_commands_p1(commands: list[list[str]]) -> tuple[int, int]:
        """Part 1: Uses the list of commands to calculate the final horizontal 
        position and depth and returns them."""
        horizontal = 0
        depth = 0
        for command in commands:
            match [command[0], int(command[1])]:
                case ['forward', magnitude]:
                    horizontal += magnitude
                case ['down', magnitude]:
                    depth += magnitude
                case ['up', magnitude]:
                    depth -= magnitude
        return horizontal, depth

Here I got to use the new `match` and `case` structural pattern matching. It worked out well because I didn't have to deal with splitting the command into it's direction and magnitude components, the pattern matching handled that for me! I'd definitely like to explore this new feature in depth in future as it seems extremely powerful.

### Part 2

Part 2 was very similar to part 1 but the way that depth was calculated changed. It was now the product of a new variable `aim` and the `horizontal` distance. I would have liked to have refactored the function used for part 1 to also work with part 2 but I couldn't think of a nice way of doing it so I created an entirely new function for part 2 still using the same principles as part 1.

    :::py
    def follow_commands_p2(commands: list[list[str]]) -> tuple[int, int]:
        """Part 2: Uses the list of commands to calculate the final horizontal
        position and depth and returns them. For part 2 depth is determined
        by aim and horizontal movement."""
        horizontal = 0
        depth = 0
        aim = 0
        for command in commands:
            match [command[0], int(command[1])]:
                case ['forward', magnitude]:
                    horizontal += magnitude
                    depth += magnitude * aim
                case ['down', magnitude]:
                    aim += magnitude
                case ['up', magnitude]:
                    aim -= magnitude
        return horizontal, depth

### Summary 

Finally putting it all together.

    :::py
    if __name__ == "__main__":
        input_file_path = pathlib.Path(__file__).parent / "input.txt"
        commands = parse_input(input_file_path)

        horizontal, depth = follow_commands_p1(commands)
        print(f"Part 1: {horizontal * depth}")

        horizontal, depth = follow_commands_p2(commands)
        print(f"Part 2: {horizontal * depth}")    

Already 2/2 on using new features of python 3.10 which is great! Hopefully that continues moving forwards. The only thing I don't like about my solution for this one is the amount of duplicated code in the functions for part 1 and part 2. If anybody has any suggestions for how this could be refactored please get in touch via e-mail or twitter. Contact details be found [here]({filename}/pages/about.md).

***Links***

If you want to take part here is the link for [day 2](https://adventofcode.com/2021/day/2).

My solution can be found on [github](https://github.com/rosswf/AdventOfCode2021/blob/main/day2/solution.py).