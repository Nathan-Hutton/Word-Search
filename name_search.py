import numpy as np 
import argparse
import string

class NameSearch:

    def __init__(self, Name_List, Name_Algorithm, Name_Length):
        # Matrix of the word search puzzle 
        self.matrix = np.load("data/matrix.npy")
        # Name of the algorithm
        self.Name_Algorithm = Name_Algorithm
        # Length of the name
        self.Name_Length = Name_Length
        # List of all potential names 
        with open("./data/names/"+Name_List+".txt", 'r') as f:
            self.names = f.read().splitlines()
        self.names = [n.upper().strip() for n in self.names]

    def match_BruteForce(self, pattern, text):
        front_index = 0
        back_index = self.Name_Length
        while back_index <= len(text):
            slider = "".join(text[front_index:back_index])
            match = True
            for i in reversed(range(len(slider))):
                if pattern[i] != slider[i]:
                    match = False
                    break
            if match:
                print(slider)
            front_index += 1
            back_index += 1

    def match_Horspool(self, pattern, text):
        alphabet = string.ascii_uppercase
        shift_table = {}
        for letter in alphabet:
            shift_table[letter] = len(pattern)
            for i in range(len(pattern) - 1):
                if pattern[i] == letter:
                    shift_table[letter] = len(pattern) - 1 - i

        front_index = 0
        back_index = self.Name_Length
        while back_index <= len(text):
            slider = "".join(text[front_index:back_index])
            current_letter = slider[-1]
            if pattern[-1] != current_letter:
                front_index += shift_table[current_letter]
                back_index += shift_table[current_letter]
                continue
            if pattern[-1] == current_letter:
                match = True
                for i in reversed(range(len(slider) - 1)):
                    if pattern[i] != slider[i]:
                        front_index += shift_table[current_letter]
                        back_index += shift_table[current_letter]
                        match = False
                        break
                if match:
                    print(slider)
                    break


    def search(self):
        # pattern is each name in self.names
        # text is each horizontal, vertical, and diagonal strings in self.matrix
        rows, columns = self.matrix.shape
        names_to_check = [name for name in self.names if len(name) == self.Name_Length]
        if self.Name_Algorithm == "BruteForce":
            # Create list of names of a certain length
            for name in names_to_check:
                # Check rows
                for row in range(rows):
                    self.match_BruteForce(name, self.matrix[row, :])

                # Check columns
                for column in range(columns):
                    self.match_BruteForce(name, self.matrix[:, column])

                # Check diagonals from top left to bottom right
                for row_index in reversed(range(rows)):
                    text_list = []
                    for i in range(rows - row_index):
                        text_list.append(self.matrix[row_index + i, i])
                    self.match_BruteForce(name, text_list)

                for column_index in reversed(range(1, columns)):
                    text_list = []
                    for i in range(columns - column_index):
                        text_list.append(self.matrix[i, column_index + i])
                    self.match_BruteForce(name, text_list)

                # Check diagonals from top right to bottom left
                for row_index in range(rows):
                    text_list = []
                    for i in range(row_index + 1):
                        text_list.append(self.matrix[i, row_index - i])
                    self.match_BruteForce(name, text_list)

                for column_index in reversed(range(1, columns)):
                    text_list = []
                    row_index = columns - 1 - column_index
                    for i in range(1, column_index + 1):
                        text_list.append(self.matrix[row_index + i, columns - i])
                    self.match_BruteForce(name, text_list)

        elif self.Name_Algorithm == "Horspool":
            for name in names_to_check:
                # Check rows
                for row in range(rows):
                    self.match_Horspool(name, self.matrix[row, :])

                # Check columns
                for column in range(columns):
                    self.match_Horspool(name, self.matrix[:, column])

                # Check diagonals from top left to bottom right
                for row_index in reversed(range(rows)):
                    text_list = []
                    for i in range(rows - row_index):
                        text_list.append(self.matrix[row_index + i, i])
                    self.match_Horspool(name, text_list)

                for column_index in reversed(range(1, columns)):
                    text_list = []
                    for i in range(columns - column_index):
                        text_list.append(self.matrix[i, column_index + i])
                    self.match_Horspool(name, text_list)

                # Check diagonals from top right to bottom left
                for row_index in range(rows):
                    text_list = []
                    for i in range(row_index + 1):
                        text_list.append(self.matrix[i, row_index - i])
                    self.match_Horspool(name, text_list)

                for column_index in reversed(range(1, columns)):
                    text_list = []
                    row_index = columns - 1 - column_index
                    for i in range(1, column_index + 1):
                        text_list.append(self.matrix[row_index + i, columns - i])
                    self.match_Horspool(name, text_list)

if __name__ == "__main__":
        
    parser = argparse.ArgumentParser(description='Word Searching')
    parser.add_argument('-name', dest='Name_List', required = True, type = str, help='Name of name list')
    parser.add_argument('-algorithm', dest='Name_Algorithm', required = True, type = str, help='Name of algorithm')
    parser.add_argument('-length', dest='Name_Length', required = True, type = int, help='Length of the name')
    args = parser.parse_args()

    # Example:
    # python name_search.py -algorithm BruteForce -name Mexican -length 5

    obj = NameSearch(args.Name_List, args.Name_Algorithm, args.Name_Length)
    obj.search()
    # obj.match_BruteForce('jason', 'something')


