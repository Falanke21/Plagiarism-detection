#!/usr/bin/python

# This program should be used with Python 3.6 or newer versions
# This program was tested working on a Windows 10 PC, Python 3.7
# Some assumptions:
# Assume commandline arguments are in correct order.
# Assume the tuple_size n is less than or equal to number of words in both input files
# (If no, this program will exit with a message saying tuple_size should be less).
# Assume the only two punctuations in files are "." and ",".
# (This can be easily changed. See method remove_punctuation)

import itertools  # for a cartesian product
import sys  # system command line
from typing import Dict, List  # type hints


class PlagiarismDetector:
    def __init__(self, tuple_size: int):
        # the size of tuple, default is 3
        self.tuple_size = tuple_size

        # this set refers to all n-word tuples appeared in file2
        self.file2_set = set()

        # dictionary for synonyms, key=the word, value=tuple of synonyms of the word(including the word itself)
        self.syns_dict: Dict[str, tuple] = {}

    def process_synonym(self, syns_file: str) -> None:
        """
        Read all synonyms from the synonym file and store them inside self.syns_dict
        :param syns_file: The name of the synonym file
        """
        with open(syns_file) as fsyns:
            for line in fsyns:
                # change paragraph into a list of words
                line = line.split()
                for item in line:
                    if item in self.syns_dict:  # if the word is already a synonym
                        self.syns_dict[item] += tuple(line)
                    else:
                        self.syns_dict[item] = tuple(line)

    def create_tuple_set(self, file_name2: str) -> None:
        """
        Read from input file2, and store all n-size tuples inside a set called self.file2_set
        By using this set, we can determine whether a tuple appeared in input file2 in O(1) time(average case).
        :param file_name2: The name of input file2
        """
        with open(file_name2) as file2:
            read_result = file2.read()

        read_result = self.remove_punctuations(read_result)
        # change paragraph into a list of words
        read_result = read_result.split()
        if self.tuple_size > len(read_result):
            print("Tuple size should be less than " + str(len(read_result)))
            sys.exit(1)

        # We loop (number of words - tuple_size) times.
        # Each iteration we create a word tuple and add it to our set.
        for i in range(len(read_result) - self.tuple_size + 1):
            self.file2_set.add(tuple(read_result[i: i + self.tuple_size]))

    def remove_punctuations(self, s: str) -> str:
        # Assume the only two punctuations in files are "." and ","
        s = s.replace(".", "")
        s = s.replace(",", "")
        # s = s.replace("!", "")
        # s = s.replace("?", "")
        # s = s.replace("'", "")
        # s = s.replace('"', '')
        # add more punctuation elimination if needed

        return s

    def produce_output(self, file_name1: str) -> str:
        """
        This method reads from input file1, and check every tuple in file1 whether it(or it's synonyms)
        appears in file2. Returns the final result by counting the number of duplicate/plagiarism.
        :param file_name1: The name of input file1
        :return: The final result, the percent of tuples in file1 which appear in file2
        """
        with open(file_name1) as file1:
            read_result = file1.read()
        read_result = self.remove_punctuations(read_result)
        read_result = read_result.split()

        if self.tuple_size > len(read_result):
            print("Tuple size should be less than " + str(len(read_result)))
            sys.exit(1)

        # total number of tuples in file1
        total_counter = len(read_result) - self.tuple_size + 1
        duplicate_counter = 0

        # loop through all tuples in file1
        for i in range(total_counter):
            # list all synonym-tuples of the current tuple
            combinations = self.look_up_combinations(read_result[i:i + self.tuple_size])
            for tup in combinations:
                if tup in self.file2_set:
                    # a plagiarism is detected
                    duplicate_counter += 1
                    break

        # assume total_counter is not 0
        final_result = int(100 * (duplicate_counter / total_counter))
        return str(final_result) + "%"

    def look_up_combinations(self, current_n_words: List[str]) -> List[tuple]:
        """
        Find all synonym-tuples of current_n_words
        :param current_n_words: Current word tuple. Length is equal to self.tuple_size
        :return: The list of all synonym-tuples of current_n_words.
        """
        # We create a list of tuple.
        # Each tuple denotes all synonyms of word at index i in current_n_words.
        # For ex, current_n_words = ["a", "jog"], n_synonyms will be [("a",), ("jog", "run")]
        # if "jog" and "run" are synonyms.
        n_synonyms: List[tuple] = []
        for word in current_n_words:
            if word in self.syns_dict:
                # If there exist at least one synonym of this word
                n_synonyms.append(self.syns_dict[word])
            else:
                n_synonyms.append((word,))

        # Generate all synonym-tuples of current_n_words
        combinations = list(itertools.product(*n_synonyms))
        return combinations


if __name__ == "__main__":
    # check the number of command line arguments
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python plagiarism_detect.py syns.txt input_file1 input_file2 (tuple_size=3)")
        sys.exit(1)

    DEFAULT_TUPLE_SIZE = 3
    synonym_filename = sys.argv[1]
    input_file1 = sys.argv[2]
    input_file2 = sys.argv[3]
    # Checking for the optional commandline argument
    n = int(sys.argv[4]) if len(sys.argv) == 5 else DEFAULT_TUPLE_SIZE

    pd = PlagiarismDetector(n)
    pd.process_synonym(synonym_filename)
    pd.create_tuple_set(input_file2)
    print(pd.produce_output(input_file1))
