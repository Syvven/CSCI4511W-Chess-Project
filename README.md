# CSCI4511W Final Project

## Chess -- Will be updated in future

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

Step 3: cd into the proper directory containing the `chess-final-for-now.py` file

Step 4: In terminal, type:

`> python3 chess-final-for-now.py`
