# CSCI4511W Final Project

## Chess -- Currently Being Updated -- Expected to Finish Sometime This Weekend (5/6/22)

This repository contains the files to run a game of chess created by myself (Noah Hendrickson) for the CSCI 4511W Intro to Artificial Intelligence final project. The game is written in python and the graphics utilize turtle's python library. 

## What Is Included In This Repository

Files included in this repository include:

- `old-files`: Old program files that have since been updated
  - `lauren-pieces`
    - contains sprites for the pieces, recolored by Lauren Oliver
  - `chess-final-for-now.py`
    - contains all the code needed to run the game
    - this iteration lacks a couple features and has a non-functional AI version
- `updated-files`: The new directory for the main program
  - `lauren-pieces`
    - contains sprites for the pieces, recolored by Lauren Oliver
  - `chess.py`
    - contains main code to setup the chess game
  - `piece.py`
    - contains Piece class definition for information on individual pieces
  - `board.py`
    - contains the Board class definition as well as most of the functional code
  - `move.py`
    - contains Move class definition to contain information on moves
- `Final-Report.pdf`
  - contains an 11 page report that includes:
    - A history of chess AI and algorithms
    - The process of creating this program
    - Experiments done on this program and other chess AIs
    - Analysis of results

## Features

This chess program is an almost completely functional chess game. There are a few features that aren't included:

- Third AI version is somewhat slow
- Stalemate not entirely implemented

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
  - The evaluation of the board is influenced by:
    - Pieces on the board after a move
    - Number of opposing player's moves after a move
    - Piece being moved and destination its being moved to
    - If the move results in checkmate
- General Gameplay
  - Promoting, Castling, and En Passant
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
- Stalemates in certain circumstances
- Optional move limit

## How To Run The Game

Step 1: Install Python 3

Step 2: Install the following python libraries:

`turtle, time, math, random, copy`

Step 3: cd into the `updated-files` directory containing the `chess.py` file that is accessible by python

Step 4: In terminal, type:

`> python3 chess.py <mode> <ai_version>`

- mode: 
  - two-player: will initiate a game that can be played by two human players
  - ai: will initiate a game where human plays as white, and an AI plays as black
- ai_version: 
  - 0: input for two-player mode
  - 1: completely random ai moves
  - 2: ai moves utilize heuristic function with no search
  - 3: ai moves utilize minimax with alpha-beta pruning

## How to Play The Game

- When the file has been run, select the piece you wish to move and the available moves will be highlighted. 
- Select the square you wish to move the piece to
- If you wish to select a different piece, right click
- At most points, you can hit the 'z' key in order to undo the previous move. 
  - The AI will not move again if you undo its move, so you will have to undo two moves at a time
- If you hit the 'r' key, you will restart the game from fresh
- If you hit the 'q' key, the game will be over, press 'q' again to quit or restart using 'r'
- Play the game until a player is in checkmate
- Once this occurs, a notification will pop up, from which you can restart using 'r' or quit using 'q'

## Known Issues

- Minimax search is slow
- No stalemate for certain circumstances
- Not implemented many aspects of a good board evaluation, thus the AI is not great


