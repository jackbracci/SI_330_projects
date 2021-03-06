# docdist7.py
# Authors: Ronald L. Rivest, Erik Demaine
# Some adaptation for SI 330 by Kevyn Collins-Thompson
# Additional adaptation for SI 330 by Matthew Kay
#
# Changelog:
#   Version 1: 
#     Initial version
#   Version 2:
#     Added profiling to get routine timings
#   Version 3:
#     Changed concatenate to extend in get_words_from_line_list
#   Version 4:
#     Changed count_frequency to use dictionaries instead of lists
#   Version 5:
#     Change get_words_from_string to use string translate and split
#   Version 6:
#     Changed sorting from insertion sort to merge sort
#   Version 7:
#     Remove sorting altogether via more hashing
#
# Usage:
#    docdist7.py filename1 filename2
#     
# This program computes the "distance" between two text files
# as the angle between their word frequency vectors (in radians).
#
# For each input file, a word-frequency vector is computed as follows:
#    (1) the specified file is read in
#    (2) it is converted into a list of alphanumeric "words"
#        Here a "word" is a sequence of consecutive alphanumeric
#        characters.  Non-alphanumeric characters are treated as blanks.
#        Case is not significant.
#    (3) for each word, its frequency of occurrence is determined
#    (4) the word/frequency lists are sorted into order alphabetically
#
# The "distance" between two vectors is the angle between them.
# If x = (x1, x2, ..., xn) is the first vector (xi = freq of word i)
# and y = (y1, y2, ..., yn) is the second vector,
# then the angle between them is defined as:
#    d(x,y) = arccos(inner_product(x,y) / (norm(x)*norm(y)))
# where:
#    inner_product(x,y) = x1*y1 + x2*y2 + ... xn*yn
#    norm(x) = sqrt(inner_product(x,x))

import math
# math.acos(x) is the arccosine of x.
# math.sqrt(x) is the square root of x.

import string
# string.join(words,sep) takes a given list of words,
#    and returns a single string resulting from concatenating them
#    together, separated by the string sep .
# string.lower(word) converts word to lower-case

import sys


##################################
# Operation 1: read a text file ##
##################################
def read_file(filename):
    """ 
    Read the text file with the given filename;
    return a list of the lines of text in the file.
    """
    try:
        with open(filename) as file:
            line_list = file.readlines()
    except IOError as e:
        print(e)
        print("Error opening or reading input file: " + filename)
        sys.exit()
    return line_list


#################################################
# Operation 2: split the text lines into words ##
#################################################
def get_words_from_line_list(line_list):
    """
    Parse the given list L of text lines into words.
    Return list of all words found.
    """

    word_list = []
    for line in line_list:
        words_in_line = get_words_from_string(line)
        # Using "extend" is much more efficient than concatenation here:
        word_list.extend(words_in_line)
    return word_list


# global variables needed for fast parsing
# translation table maps upper case to lower case and punctuation to spaces
translation_table = str.maketrans(string.punctuation + string.ascii_uppercase,
                                  " " * len(string.punctuation) + string.ascii_lowercase)


def get_words_from_string(line):
    """
    Return a list of the words in the given input string,
    converting each word to lower-case.

    Input:  line (a string)
    Output: a list of strings 
              (each string is a sequence of alphanumeric characters)
    """
    line = line.translate(translation_table)
    word_list = line.split()
    return word_list


##############################################
# Operation 3: count frequency of each word ##
##############################################
def count_frequency(word_list):
    """
    Return a dictionary mapping words to frequency.
    """
    word_frequencies = {}
    for new_word in word_list:
        if new_word in word_frequencies:
            word_frequencies[new_word] += 1
        else:
            word_frequencies[new_word] = 1
    return word_frequencies


#############################################
## compute word frequencies for input file ##
#############################################
def word_frequencies_for_file(filename):
    """
    Return dictionary of (word,frequency) pairs for the given file.
    """

    line_list = read_file(filename)
    word_list = get_words_from_line_list(line_list)
    freq_mapping = count_frequency(word_list)

    print("File", filename, ":",
          len(line_list), "lines,",
          len(word_list), "words,",
          len(freq_mapping), "distinct words")

    return freq_mapping


def inner_product(dict_1, dict_2):
    sum_ = 0.0
    for key in dict_1:
        if key in dict_2:
            sum_ += dict_1[key] * dict_2[key]
    return sum_


def vector_angle(dict_1, dict_2):
    """
    The input is a list of (word,freq) pairs, sorted alphabetically.

    Return the angle between these two vectors.
    """
    numerator = inner_product(dict_1, dict_2)
    denominator = math.sqrt(inner_product(dict_1, dict_1) * inner_product(dict_2, dict_2))
    return math.acos(numerator / denominator)


def main():
    if len(sys.argv) != 3:
        print("Usage: docdist7.py filename_1 filename_2")
    else:
        filename_1 = sys.argv[1]
        filename_2 = sys.argv[2]
        sorted_word_list_1 = word_frequencies_for_file(filename_1)
        sorted_word_list_2 = word_frequencies_for_file(filename_2)
        distance = vector_angle(sorted_word_list_1, sorted_word_list_2)
        print("The distance between the documents is: %0.6f (radians)" % distance)


if __name__ == "__main__":
    import profile

    profile.run("main()")
