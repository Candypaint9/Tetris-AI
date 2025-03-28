# Tetris AI
## Overview
This project implements an AI agent that plays Tetris by taking real-time decisions using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The goal is to evolve neural networks that can effectively learn and improve their gameplay over generations.
## Features

- <b>Tetris Environment:</b>  A simulated Tetris game where the AI agent makes decisions.
- <b>NEAT Implementation:</b>  Uses the NEAT algorithm to evolve neural network controllers.
- <b>Real-Time Decision Making: </b>The evolved agent makes gameplay decisions based on the current Tetris board state.
- <b>Fitness Evaluation: </b>The fitness score is evaluated on the basis of gameplay perfomance based on the following features 
    <ul>
      <li>game score</li>
      <li>maximum height of columns</li>
      <li>bumpiness of columns</li>
      <li>gaps in the board and the lines cleared</li> 
    </ul> 
   

## Requirements

- <b>Python 3.7+</b></li>
- <b>Python Libraries:</b>
  <ul>
    <li>numpy</li>
    <li>pygame</li>
    <li>neat-python</li>
  </ul>


## How to Run
To run the Tetris AI, simply execute the script:
```bash
python runNetwork.py
```
This script initializes the Tetris environment, loads the NEAT-based neural network controller, and starts the simulation. Make sure you have installed all required dependencies(as listed in the Requirements section) before running the script.
## 

