# Simulated Prediction Market Backend

This project simulates a prediction market using the Constant Product Automated Market Maker (CPMM).
In a constant product AMM, the product of YES and NO token reserves of the market maker are held to be constant:

$$Y\times N = k$$

For instance, if a user bets 10 pounds that an event will happen, 10 yes and 10 no tokens will be
minted using this stake, and a number of tokens will be given to the user such that $k$ is held constant.
While there are many other AMM implementations as I've learned, this one was the simplest to implement in a time crunch.

## Using this API

The REST API Documentation is served at `/docs`. The user can place bets on the 4 fake markets the
server automatically creates. The implied probability (and as a result the price) will change according\
to the AMM rules.

## Trading Simulator

The server will automatically simulate some trading activity.
Specifically, four agents with `bias` and `frequency` parameters will place trades accordingly.
Also, real world events are simulated by maintaining a ground truth probability that changes randomly.
The bots will trade according to their perception of the ground truth probability,
and the implied probability the AMM calculates.

## Running the server

Optionally, create a virtual environment:

```bash
python3 -m virtualenv env
source env/bin/activate
```

Install dependencies:

```bash
pip install "fastapi[standard]"
```

Run the server:

```bash
fastapi dev main.py
```
