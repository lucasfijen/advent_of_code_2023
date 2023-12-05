import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()


def get_data(day) -> list[str]:
    """Automatically collects data from website

    If the file does not yet exist it downloads the file, otherwise it returns content

    Args:
        day (int): integer to day to collect

    Returns:
        list[str]: Returns the collected information either from file
    """
    folder = Path("./data")
    file = folder / Path(f"day_{day:02}.txt")
    if not file.exists():
        url = f"https://adventofcode.com/2023/day/{day}/input"
        print(f"File not found, downloading from: {url}")

        request = httpx.get(url, cookies={"session": os.environ.get("SESSIONCOOKIE")})
        data = request.text
        with file.open("w") as f:
            f.write(data)

    with file.open("r") as f:
        data = f.read().splitlines()

    return data


def get_example_data(day, extra="") -> list[str]:
    """Gets the example data for the day

    Args:
        day (int): day to collect

    Returns:
        list[str]: List of strings
    """

    folder = Path("./data")
    file = folder / Path(f"day_{day:02}_example{extra}.txt")

    with file.open("r") as f:
        data = f.read().splitlines()
    return data
