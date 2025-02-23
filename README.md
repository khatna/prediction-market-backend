# Simulated Prediction Market Backend

This project simulates a prediction market using the Constant Product Automated Market Maker (CPMM).
In a constant product AMM, the product of YES and NO token reserves of the market maker are held to be constant:

$$Y\times N = k$$

For instance, if a user bets 10 pounds that an event will happen, 10 yes and 10 no tokens will be
minted using this stake, and a number of tokens will be given to the user such that $k$ is held constant.
While there are many other AMM implementations as I've learned, this one was the simplest to implement in a time crunch.

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
