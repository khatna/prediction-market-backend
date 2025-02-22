from fastapi import FastAPI
from pydantic import BaseModel

from lib import market_store

from lib.models import MarketSeedData

class Bet(BaseModel):
  market_id: str
  is_yes: bool # True for buy, false for sell
  stake: float

market_store = market_store.MarketStore()

# Seed some questions
questions = [
  'Will Bitcoin hit $250k in 2025?',
  'Will it rain in London tomorrow?',
  'Will the Republicans win the 2028 election?'
]

for q in questions:
  market_store.create_market(
    MarketSeedData(
      question=q,
      initial_probability=0.5
    ),
  )
app = FastAPI()

@app.get("/markets")
def read_markets():
  return market_store.get_all_markets()

@app.get("/markets/{market_id}")
def read_market(market_id: str):
  return market_store.get_market(market_id)

@app.post("/bet")
def make_bet(bet: Bet):
  purchased = market_store.market_bet(bet.market_id, bet.is_yes, bet.stake)
  market_data = market_store.get_market(bet.market_id)
  return { 'purchased': purchased, 'market_data': market_data }
