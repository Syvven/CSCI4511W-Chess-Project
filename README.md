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
    - An AI that utilizes a minimax algorithm with alpha-beta pruning # Not completely functional
  - The evaluation of the board is influenced by:
    - Pieces on the board after a move
    - Number of opposing player's moves after a move
    - Piece being moved and destination its being moved to
    - If the move results in checkmate

## How To Run The Game
