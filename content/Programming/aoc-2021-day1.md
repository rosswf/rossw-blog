Title: Advent of Code 2021 - Day 1
Date: 2021-12-01 13:00
Tags: programming, aoc, python
Summary: Advent of Code 2021 - Day 1
Slug: aoc-2021-day1
Description: Advent of Code 2021 - Day 1
Status: hidden

It's that time of year again! 
I first took part in Advent of Code last year and made it up to day 10. I'm hoping that this year I can beat that.
I'm going to be using python 3.10 this year and my main aim is to try out some of it's new features. I won't be making modifications to my solutions after pushing them to github instead I will talk through my thought process and discussing some of the aspects that I would change. 

**Spoiler Warning: This post contains spoilers for Advent of Code Day 1.**

The challenges start out quite simple and increase in difficulty each day. This first one was quite basic but it was a lot of fun, one of my favourite parts about AoC is the story that goes alongside the challenges.

### Part 1

The first part was quite straight forward but immediately gave me the opportunity to try out something new in python 3.10 `itertools.pairwise` here is the [documentation](https://docs.python.org/3/library/itertools.html#itertools.pairwise).

The task was to read input from a text file which had a number on each line and count how many times this number increased.

First of all I defined a function to read the file and return a list of integers.

    :::py
    def parse_input(filename: str) -> List[int]:
        """Parses the file given by filename and returns a list of integers
        where each value in the list is a line from filename.
        """
        with open(filename) as f:
            measurements = f.readlines()
        measurements = [*map(int, measurements)]
        return measurements

I used `map` here to convert the numbers as strings to integers and returned them as a list. I'm not sure if a list comprehension would have been more efficient in this case but this approach seemed to work.

One thing that I will do in future is use `Pathlib` to ensure that the input file is always being read relative to the python file.

Now that I had my list of integers it was time to check for values increasing.

    :::py
    def check_increasing(measurements: List[int]) -> int:
        """Pairs the values in measurements and returns how many pairs are
        increasing.
        """
        paired = pairwise(measurements)
        paired_increasing = map(lambda p: p[0] < p[1], paired)
        return sum(paired_increasing)

Here I used the new `itertools.pairwise` to group adjacent numbers together and then used `map` again but this time to check if the numbers were increasing. The `sum` of this was then returned which added up all the Truthy values.

If I were to do this again I probably would have used a generator expression instead of `map`. Something like:

    :::py
    paired_increasing = (p[0] < p[1] for p in paired)
    return(paired_increasing)

### Part 2

The second part was very similar to part 1 but with a little bit of added complexity which is a recurring theme for AoC challenges. For this part it was required to check if the sum of 3 adjacent numbers was increasing or decreasing. 
Luckily I'd written my code in such a way that I could re-use my `check_increasing` function from part 1 so I just needed to create a solution for summing 3 adjacent numbers.

    :::py
    def get_three_measurement_sums(measurements: List[int]) -> List[int]:
        """Takes a list of measurements and returns the sums of each 3 consecutive
        values in the list.
        """
        measurement_sums = [
            measurements[i - 2] + measurements[i - 1] + measurements[i]
            for i in range(2, len(measurements))
        ]
        return measurement_sums

Here I used a list comprehension to loop through the list of numbers and add them together to create a new list. I'm not very happy with this at all as it seems very clumsy. I feel it would have been cleaner if I had used slicing and sum. The list this function returned could then be passed to the `check_increasing` function I created earlier for part 1.

### Summary 

Finally putting it all together.

    :::py
    if __name__ == "__main__":
        measurements = parse_input("input.txt")

        part1_solution = check_increasing(measurements)

        three_measurement_sums = get_three_measurement_sums(measurements)
        part2_solution = check_increasing(three_measurement_sums)

        print(f"Part 1: {part1_solution}")
        print(f"Part 2: {part2_solution}")

I already can't wait to see what tomorrows challenge brings. If you are taking part in Advent of Code let me know how you solved this problem or if you have any hints/tips I'd love to hear them. Get in touch via e-mail or twitter. Contact details be found [here]({filename}/pages/about.md).

***Links***

If you want to take part here is the link for [day 1](https://adventofcode.com/2021/day/1).

My solution can be found on [github](https://github.com/rosswf/AdventOfCode2021/blob/main/day1/solution.py).
