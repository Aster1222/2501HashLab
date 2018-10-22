"""Andrew Walsh, abw9yd, 13 OCT 17, wordPuzzle.cpp
The functions getWordInGrid and readInGrid, as well as the testing files, were originally written by Aaron Bloomfield in 2009 for CS2150.
This skeleton was adapted from my C++ implementation of CS2150 Lab 6: Hash Lab.
"""
import sys
import time
import HashTable

MAXROWS= 500
MAXCOLS= 500
wordsInFile = 0


# The following 8 functions are used by getWordInGrid to follow the 'direction' specified.

def N():
    global r
    r -= 1


def NE():
    global r
    global c
    r -= 1
    c += 1


def E():
    global c
    c += 1


def SE():
    global r
    global c
    r += 1
    c += 1


def S():
    global r
    r += 1


def SW():
    global r
    global c
    r += 1
    c -= 1


def W():
    global c
    c -= 1


def NW():
    global r
    global c
    r -= 1
    c -= 1


# This function pieces together the 'cardinal' functions into a dictionary for easy use
def create_switch():
    # This is meant to update global r anc c values
    # use it by calling 'result[dir]()'
    result = {
        0: N,
        1: NE,
        2: E,
        3: SE,
        4: S,
        5: SW,
        6: W,
        7: NW
    }
    return result


# Reads in the specified dictionary file and inserts every element into the given hash table.
# NOTE: In this context, 'dictionary' is like an actual dictionary, as in just a long list of words.
# It is not Python's dictionary Data Structure
def readInDict(filename, ht):
    file = open(filename, "r")
    for line in file:
        string = line.strip("\n")
        if len(string) > 2:
            ht.insert(string)
    file.close()
    return ht


# Reads in the specified grid file and returns a 2D array, as well as the number of rows and columns in that grid
def readInGrid(filename):
    file = open(filename, "r")
    rows = file.readline().strip("\n")
    cols = file.readline().strip("\n")
    data = file.readline()
    rows, cols = int(rows), int(cols)
    file.close()

    pos = 0  # the current position in the input data
    result = [[None for j in range(cols)] for i in range(rows)]
    for r1 in range(rows):
        for c1 in range(cols):
            result[r1][c1] = data[pos]
            pos += 1
    return result, rows, cols

"""
    Gets a word from the grid. words are a straight line identified by a starting row and column, direction, and length.
    startRow and startCol specify the row and column to start at.
    dir specifies which direction in the grid to look for the next character in the word.
    len specifies how many letters are in the word, so the function knows when to stop.
"""
def getWordInGrid(startRow, startCol, dir, len, numRows, numCols):
    global output, grid, switch, r, c
    if len >= 255:
        len = 255
    r = startRow
    c = startCol
    output = []
    for i in range(len):
        if (c >= numCols) or (r >= numRows) or (r < 0) or (c < 0):
            break
        output.append(grid[r][c])
        switch[dir]()
    return "".join(output)


def main():
    dict = input("Enter the dictionary filename: ")  # ex: words.txt
    grd = input("Enter the grid filename: ")  # ex: 4x7.grid.txt
    args = [dict, grd]
    global grid
    grid, rows, cols = readInGrid(args[1])  # reads the grid file into the variable 'grid'
    global switch
    switch = create_switch()
    global r, c
    r, c = 0, 0

    dict1 = open(args[0])
    size = 0
    for _ in dict1:
        size += 1  # size is the number of words in the dictionary
    dict1.close()

    hashTable = HashTable.HashTable(size, 0.2)
    hashTable = readInDict(args[0], hashTable)  # creates the Hash Table and inserts the words from the dictionary file into it.
    count = 0
    prevWord = ""
    timer = time.time()  # 'start' the timer
    longestWord = 25
    outputFile = open("out.txt", "w")
    for r1 in range(rows):
        for c1 in range(cols):
            for d in range(8):
                for l in range(3, longestWord):  # These loops iterate through each position, then in each direction and length.
                    word = getWordInGrid(r1, c1, d, l, rows, cols)

                    if word == prevWord:  # Ensures that the same word is not searched multiple times when the end of the grid is reached
                        continue
                    prevWord = word
                    test = hashTable.find(word)

                    if test:                        # Writes the found words to the file
                        outputFile.write(switch[d].__name__ + " (" + str(r1) + ", " + str(c1) + "):    " + word + "\n")
                        count += 1
    timer = time.time() - timer
    outputFile.close()
    print(str(count) + " words found")
    print("Found all words in " + str(timer) + " seconds")
    return 0


if __name__ == '__main__':
    main()
