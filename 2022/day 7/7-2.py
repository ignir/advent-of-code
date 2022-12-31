import os
import sys
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


@dataclass
class File:
    name: str
    size: int

@dataclass
class Directory:
    name: str
    parent: Optional['Directory']
    directories: Dict[str, 'Directory'] = field(default_factory=dict)
    files: Dict[str, int] = field(default_factory=dict)

    def create_child_directory(self, name):
        self.directories[name] = Directory(name, self)

    def create_file(self, name, size):
        self.files[name] = size

    @property
    def size(self):
        return sum(self.files.values()) + sum(d.size for d in self.directories.values())


class Parser:
    def build_tree(self, log_iterable: Iterable[str]):
        self._lines = list(log_iterable)
        self._current_index = 0
        self._current_dir = None
        root = Directory("/", None)
        current_dir: Directory = root

        # line = self._advance()
        while not self._is_at_end:
            if self._current_line.startswith("$ ls"):
                self._parse_ls(current_dir)
            elif self._current_line.startswith("$ cd"):
                dst = self._current_line[5:]
                if dst == "/":
                    current_dir = root
                elif dst == "..":
                    if not current_dir.parent:
                        raise Exception("Attempting to '..' from a directory with no parent.")
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.directories[dst]
                line = self._advance()
            else:
                raise Exception(f"Unexpected line: '{line}'")

        return root

    def _parse_ls(self, directory: Directory):
        while not self._is_at_end and not (line := self._advance()).startswith("$"):
            if line.startswith("dir"):
                child_directory_name = line.split()[1]
                directory.create_child_directory(child_directory_name)
            else:
                size, file_name = line.split()
                size = int(size)
                directory.create_file(file_name, size)

    def _advance(self):
        if self._is_at_end:
            return None
        self._current_index += 1
        return self._current_line

    @property
    def _current_line(self):
        return self._lines[self._current_index]

    @property
    def _peek_line(self):
        if self._is_at_end:
            return None
        return self._lines[self._current_index + 1]

    @property
    def _is_at_end(self):
        return self._current_index == len(self._lines) - 1


def filter_directories(root: Directory, condition) -> List[Directory]:
    filtered = []
    if condition(root):
        filtered.append(root)
    for child in root.directories.values():
        filtered.extend(filter_directories(child, condition))
    return filtered


def part1():
    log = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    tree = Parser().build_tree(log)

    small_dirs = filter_directories(tree, lambda d: d.size <= 100000)
    print(f"Sum of total sizes is {sum(d.size for d in small_dirs)}")


def part2():
    log = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    tree = Parser().build_tree(log)

    TOTAL_SPACE = 70_000_000
    FREE_SPACE_REQUIRED = 30_000_000
    unused_space = TOTAL_SPACE - tree.size
    space_to_be_freed = FREE_SPACE_REQUIRED - unused_space

    candidates = filter_directories(tree, lambda d: d.size >= space_to_be_freed)
    print(f"Size of the directory to be deleted is {min(d.size for d in candidates)}")


part1()
part2()
