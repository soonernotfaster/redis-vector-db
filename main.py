import os
from bs4 import BeautifulSoup

FILENAME = "../soonernotfaster/content/posts/writing-maybe-in-ruby-lessons-learned.md"
def main() -> None:
    lines = None
    abs_filepath = os.path.abspath(FILENAME)
    with open(abs_filepath, "r") as f:
        lines = f.readlines()

    print(lines)


if __name__ == "__main__":
    main()
