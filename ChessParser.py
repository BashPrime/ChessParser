#!/usr/bin/env python
# Evan Taylor
# ChessParser.py
# Originally programmed for a COMP 421 lab assignment at CSU Channel Islands

import xml.etree.ElementTree as ET

# Function that checks if the knight can move to the space [otherRow][otherCol] from its given position [thisRow][thisCol].
# returns True if it can, False if it cannot
def checkKnightMoves(table, thisRow, thisCol, otherRow, otherCol):
    canDo = False
    if (otherRow >= 0 and otherRow < len(table)) and (otherCol >= 0 and otherCol < len(table[otherRow])):
        if not ((table[thisRow][thisCol].isupper() and table[otherRow][otherCol].isupper()) or (table[thisRow][thisCol].islower() and table[otherRow][otherCol].islower())):
            canDo = True
    return canDo


# Initialize XML tree/hierarchy for parsing
tree = ET.parse('gamedb.txt')
games = tree.getroot()

# Add game elements to dictionary for easier access
for game in games:
    gameDict = {}
    for f in game:
        gameDict[f.tag] = f

    # Print the text game information
    print '-'*80
    print gameDict['white'].text + ' vs. ' + gameDict['black'].text + ' at ' + gameDict['event'].text + ' on ' + gameDict['date'].text
    print 'The opening played is (' + gameDict['opening'].get('book') + ') ' + gameDict['opening'].text
    
    if gameDict['result'].text == '1-0':
        winner = 'White'

    else:
        winner = 'Black'

    print winner + ' wins this game'



    # Set up the chess table and split the moves into iterable rows
    chessTable  = [['.' for x in xrange(8)] for x in xrange(8)]
    moves = gameDict['fen'].text.split('/')

	# Because the first row of moves is row 8 in the chess table, we iterate through the chess table in reverse while iterating normally through the moves list.
	# The reverse iteration is accomplished by offsetting the length of the chess table with the current row that moves is on in the loop.
    for row in range(len(moves)):
        chessIter = 0
        for char in moves[row]:
            #If a number is found, iterate spaces by that number in the row
            if char.isdigit():
                chessIter += int(char)

            #If an [A-Za-z] character is found instead, set element to character and iterate by one
            elif char.isalpha() and chessIter < len(chessTable[row]):
                chessTable[len(chessTable) - 1 - row][chessIter] = char
                chessIter += 1


    print 'Here is the position at move ' + gameDict['fen'].get('move') + '\n'
    
    # Print the chess table
    print '   a b c d e f g h'
    for row in reversed(range(len(chessTable))):
        print str(row + 1) + ' ',
        for col in range(len(chessTable[row])):
            print chessTable[row][col],
        print ''



    # Print the knight moves
    print '\nHere are the legal knight moves:'
    rowLabels = ['1', '2', '3', '4', '5', '6', '7', '8']
    colLabels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    for row in reversed(range(len(chessTable))):
        for col in range(len(chessTable[row])):
            if chessTable[row][col] == 'N' or chessTable[row][col] == 'n':
                print 'N' + colLabels[col] + rowLabels[row] + ':',

                if checkKnightMoves(chessTable, row, col, row-1, col-2):
                    print 'N' + colLabels[col-2] + rowLabels[row-1],

                if checkKnightMoves(chessTable, row, col, row-2, col-1):
                    print 'N' + colLabels[col-1] + rowLabels[row-2],

                if checkKnightMoves(chessTable, row, col, row-2, col+1):
                    print 'N' + colLabels[col+1] + rowLabels[row-2],

                if checkKnightMoves(chessTable, row, col, row-1, col+2):
                    print 'N' + colLabels[col+2] + rowLabels[row-1],

                if checkKnightMoves(chessTable, row, col, row+1, col+2):
                    print 'N' + colLabels[col+2] + rowLabels[row+1],

                if checkKnightMoves(chessTable, row, col, row+2, col+1):
                    print 'N' + colLabels[col+1] + rowLabels[row+2],

                if checkKnightMoves(chessTable, row, col, row+2, col-1):
                    print 'N' + colLabels[col-1] + rowLabels[row+2],

                if checkKnightMoves(chessTable, row, col, row+1, col-2):
                    print 'N' + colLabels[col-2] + rowLabels[row+1],
               
                # For formatting purposes, print newline
                print ''
