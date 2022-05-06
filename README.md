# CSCI4511W Final Project

## Chess -- Currently Being Updated -- Expected to Finish Sometime This Weekend (5/6/22)

This repository contains the files to run a game of chess created by myself (Noah Hendrickson) for the CSCI 4511W Intro to Artificial Intelligence final project. The game is written in python and the graphics utilize turtle's python library. 

## What Is Included In This Repository

Files included in this repository include:

- `chess-final-for-now.py`
  - contains all the code necessary to run the game
- `lauren-pieces`
  - contains sprites for the pieces, recolored by Lauren Oliver
- `Final-Report.pdf`
  - contains an 11 page report that includes:
    - A history of chess AI and algorithms
    - The process of creating this program
    - Experiments done on this program and other chess AIs
    - Analysis of results

## Features

This chess program is an almost completely functional chess game. There are a few features that aren't included:

- No En Passant
- Kings can castle through, or while in, check
- Third version of the AI player is not completely finished, but somewhat functional

Features that are included:

- Graphics
  - Player can click on a piece that has valid moves, and the moves are highlighted
  - The current player's turn is noted on the right of the board
  - The colors were chosen by a design major as to be easy on the eyes and look nice
- AI Player
  - A couple iterations of an AI player can be played against:
    - An AI that plays moves at complete random
    - An AI that utilizes an evaluation function to decide moves
    - An AI that utilizes a minimax algorithm with alpha-beta pruning
      - *Not completely functional*
  - The evaluation of the board is influenced by:
    - Pieces on the board after a move
    - Number of opposing player's moves after a move
    - Piece being moved and destination its being moved to
    - If the move results in checkmate
- General Gameplay
  - Most chess moves are available to play
  - Promoting and Castling
  - Pieces with no moves cannot be selected to move
  - No time limit
    - *Might be implemented in future*
  - Stalemate is not a thing
    - I personally do not like the rule in most circumstances so I forewent it
    - Will be implemented for certain other circumstances
  - No move limit

## Planned Features

Planned features include:

- Optional time limits
- A fully functional third AI iteration
- Not being able to castle through, or out of, check
- Stalemates in certain circumstances
- Optional move limit
- En Passant

## How To Run The Game

Step 1: Install Python 3

Step 2: Install the following python libraries:

`turtle, time, math, random, copy`

Step 3: cd into the proper directory containing the `chess-final-for-now.py` file that is accessible by python

Step 4: In terminal, type:

`> python3 chess-final-for-now.py`

## How to Play The Game

- When the file has been run, select the piece you wish to move and the available moves will be highlighted. 
- Select the square you wish to move the piece to
- If you wish to select a different piece, right click
  - Depending on your mouse, it may not work because of right click being numbered differently
- At most points, you can hit the 'z' key in order to undo the previous move. 
  - The AI will not move again if you undo its move, so you will have to undo two moves at a time
- If you hit the 'r' key, you will restart the game from fresh
- If you hit the 'q' key, the program will terminate and the turtle screen will close
- Play the game until a player is in checkmate
- Once this occurs, a notification will pop up, from which you can restart using 'r' or quit using 'q'

## Known Issues



