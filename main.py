import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .src import market_store
from .src.models import MarketSeedData, MarketData, Bet, BetResponse
from .src.trading_simulator import trading_simulator

market_store = market_store.MarketStore()

# Seed some questions
questions = [
  'Will Bitcoin hit $250k in 2025?',
  'Will it rain in London tomorrow?',
  'Will the Republicans win the 2028 election?',
  'Will Liverpool win the 2025 UCL?',
]

for q in questions:
  market_store.create_market(
    MarketSeedData(
      question=q,
      initial_probability=0.5
    ),
  )

# seed some traders
simulator = trading_simulator.TradingSimulator(market_store)

@asynccontextmanager
async def lifespan(app: FastAPI):
  task = asyncio.create_task(simulator.run_simulation())
  yield
  await simulator.stop_simulation()
  await task

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/markets")
def read_markets() -> list[MarketData]:
  return market_store.get_all_markets()

@app.get("/markets/{market_id}")
def read_market(market_id: str) -> MarketData:
  return market_store.get_market(market_id)

@app.post("/bet")
def make_bet(bet: Bet) -> BetResponse:
  purchased = market_store.market_bet(bet.market_id, bet.is_yes, bet.stake)
  market_data = market_store.get_market(bet.market_id)
  return { 'purchased': purchased, 'market_data': market_data }
