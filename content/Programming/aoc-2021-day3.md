Title: Personal Update & Advent of Code 2021 - Day 3
Date: 2022-05-22 18:30
Tags: programming, aoc, python, personal
Summary: Advent of Code 2021 - Day 3
Slug: aoc-2021-day3
Description: Advent of Code 2021 - Day 3
Status: hidden

### Personal Update

As you can see the plan to follow along with Advent of Code 2021 each day in December didn't quite work it. Programming and blogging had to take a back seat for a while due to personal reasons, part of which was starting a new job.
This new chapter is extremely exciting but for a while I didn't have much free time however I am now back to programming and what better way to get back into it than to pick up where I left off with Advent of Code, so let's
get into Day 3!

**Spoiler Warning: This post contains spoilers for Advent of Code Day 3.**

As you may remember from my [first post]({filename}/Programming/aoc-2021-day1.md) on Day 1 the plan initially was to try to utilise as many of the new features of python 3.10 as a I could. However it's been quite a few months
since I've touched python so I'm going to relax this self-imposed constraint and just take things as they come until I can get back into the swing of things. The quality of my code may also be a little lacking for a bit but I can
live with that, these things unfortunately do happen and I'm extremely out of practice.

### Part 1

The input for this challenge is a report, each line consisting of a binary number..

The task for part 1 was to calculate the power consumption which is the product of the Gamma Rate and Epsilon Rate. The Gamma Rate is calculated by taking the most common bit (1 or 0) from each position/column within the report. The Epsilon Rate is the inverse of this and uses the least common bit.

First of all I defined a function to read the file and parse the input. Thankfully there wasn't really much parsing that needed to be performed for this challenge as each value from the report was on it's own line so it was sufficient to read all the lines and then strip the new line characters. I kept the binary numbers as strings as it made it easier for me to iterate over them and check the values in each position.

    :::py
    def parse_input(filename: pathlib.Path) -> list[str]:
        """Parses the file given by filename and returns the report as a list of numbers
        as strings.
        """
        with open(filename) as f:
            report = f.readlines()
        report = [number.strip() for number in report]
        return report

Now that I have the report as a list of strings I can start by getting the most common bits in each position for the Gamma Rate. I used zip to transpose the report to make it possible to count how many 0's and 1's there were in a given position.

    :::py
    def get_most_common_bits(report: list[str]) -> str:
        """Takes the report and calculates the most common bits in each column,
        this is then returned as a string.
        """
        transposed = zip(*report)
        most_common_bits = "".join(
            "1" if number.count("1") >= number.count("0") else "0" for number in transposed
        )
        return most_common_bits

Then for the Epsilon Rate I need the least common bits. I thought the easiest way to do this was just to flip the bits used for the Gamma Rate.

    :::py
    def get_least_common_bits(most_common_bits: str) -> str:
        """Uses the number from most_common_bits and flips each bit to return
        the least common bits in each column as a string.
        """
        least_common_bits = "".join("1" if n == "0" else "0" for n in most_common_bits)
        return least_common_bits

After this it was just a case of putting it all together. Converting the binary numbers as strings to integers and then multiplying them together to get the power consumption.

    :::py
    def part_1(report: list[str]) -> None:
        """Uses the report to calculate the answer for part 1."""
        most_common_bits = get_most_common_bits(report)
        least_common_bits = get_least_common_bits(most_common_bits)

        gamma_rate = int(most_common_bits, 2)
        epsilon_rate = int(least_common_bits, 2)

        power_consumption = gamma_rate * epsilon_rate

        print(f"Part 1: {power_consumption}")

### Part 2

As is typical for part 2 of Advent of Code it builds on Part 1. The goal of this part was to calculate the life support rating. This is the product of the Oxygen Generator Rating and the CO2 Scrubber Rating.
Each of these are calculated in a similar way. For the Oxygen Generator Rating the most common bit in each position is calculated and then values that do not have this bit are removed from the report. This is repeated for the 2nd position, 3rd position etc. until there is only one value left which is the Oxygen Generator Rating. This was complicated a little bit as the most common bit had to be calculated on the report *after* values had been removed so it was not as simple as using the value from Part 1. The Advent of Code instructions provide a better explanation of this process than I can.

The CO2 Scrubber Rating is the same as the Oxygen Generator Rating but using the least common bit.

First I'll start with the Oxygen Generator Rating. This is where how rusty I am with python really showed itself. I'm sure that this could be done in a simpler and efficient manner. I basically looped through each position, calculated the most common bit at that point, then built a new list containing only the values that contained the most common bit in this position. I then iterated over the new list for the next position and repeated this process until there was only one value left.

I had to add a guard clause to return if there was only one value left in the report as this could happen before reaching the final position.

    :::py
    def get_oxygen_rating(report: list[str]) -> str:
        """Calculates the oxygen rating from the report using the most_common_bits function
        to filter out numbers that only contain the most common bit in each position
        until only one number is left. Each time numbers are filtered out, the most common bit is recalculated on the remaining
        numbers from the report for a given position.
        """
        for i in range(len(report[0])):
            if len(report) == 1:
                return report[0]

            most_common_bits = get_most_common_bits(report)
            working_report = [
                number for number in report if number[i] == most_common_bits[i]
            ]
            report = working_report[:]
        return working_report[0]

Then for the CO2 Scrubber Rating it was very similar but because of how I had setup the process of finding the least common bits I had to calculate the most common bits each time and then flip them. There is also a lot of repition between this function and the previous one so I'm sure some of this could be refactored. However since it was only repeated twice I think it's okay, if there were three or more functions with very similar code I definitely would have refactored.

    :::py
    def get_co2_rating(report: list[str]) -> str:
        """Calculates the co2 rating from the report using the least_common_bits function
        to filter out numbers that only contain the least common bit in each position until only
        one number is left. Each time numbers are filtered out, the least common bit is
        recalculated on the remaining numbers from the report for a given position.
        """
        for i in range(len(report[0])):
            if len(report) == 1:
                return report[0]

            most_common_bits = get_most_common_bits(report)
            least_common_bits = get_least_common_bits(most_common_bits)
            working_report = [
                number for number in report if number[i] == least_common_bits[i]
            ]
            report = working_report[:]
        return report[0]

Then putting it together and multiplying the Oxygen Generator Rating and CO2 Scrubber Rating.

    :::py
    def part_2(report: list[str]) -> None:
        """Uses the report to calculate the answer for part 2."""
        oxygen_rating = int(get_oxygen_rating(report), 2)
        co2_rating = int(get_co2_rating(report), 2)

        life_support_rating = oxygen_rating * co2_rating

        print(f"Part 2: {life_support_rating}")

### Summary 

Then finally actually running all the code to calculate the solutions.

    :::py
    if __name__ == "__main__":
        test_file_path = pathlib.Path(__file__).parent / "test_input.txt"
        input_file_path = pathlib.Path(__file__).parent / "input.txt"

        report = parse_input(input_file_path)

        part_1(report)
        part_2(report)

It feels great to finally get back into Python again and write some code, I'm definitely aware of the need to improve my problem solving skills but that's the whole purpose of Advent of Code. If anybody has any suggestions for how this could be made more efficient please get in touch via e-mail or twitter. Contact details be found [here]({filename}/pages/about.md).

***Links***

If you want to take part here is the link for [day 3](https://adventofcode.com/2021/day/3).

My solution can be found on [github](https://github.com/rosswf/AdventOfCode2021/blob/main/day3/solution.py).
