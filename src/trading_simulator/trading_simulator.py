import asyncio
import math
import random
from dataclasses import dataclass

from .. import market_store

@dataclass
class SimulatedTrader:
  name: str
  bias: float  # Tendency to bet yes (0-1)
  activity_level: float  # Probability they decide to trade
  
  async def decide_trade(self, ground_truths, market_data):
    if random.random() > self.activity_level:
      return None
            
    perceived_probability = (ground_truths[market_data.id] + self.bias) / 2    
    is_yes = perceived_probability > market_data.probability
    stake = round(random.uniform(5, 20), 2)

    return {
        'market_id': market_data.id,
        'is_yes': is_yes,
        'stake': stake
    }

class TradingSimulator:
  def __init__(self, market_store: market_store.MarketStore):
    self.ground_truths = dict()
    self.market_store = market_store
    self.traders = [
      SimulatedTrader("Optimist", bias=0.8, activity_level=0.3),
      SimulatedTrader("Pessimist", bias=0.2, activity_level=0.3),
      SimulatedTrader("Balanced", bias=0.5, activity_level=0.5),
      SimulatedTrader("FrequentTrader", bias=0.5, activity_level=0.8),
    ]
    self.is_running = False
    for market in market_store.get_all_markets():
      self.ground_truths[market.id] = market.probability
  
  def update_ground_truth(self, market_id):
    # Every 10 cycles or so, simulate a real world event
    # changing the ground truth probability
    r = random.random()
    if r > 0.1:
      return
    sign = 1 if r < 0.05 else -1
    pct_change = random.uniform(5, 10) * sign
    new_prob = self.ground_truths[market_id] + pct_change / 100
    self.ground_truths[market_id] = min(max(new_prob, 0), 1)

  async def run_trading_cycle(self):
    print(self.ground_truths)
    markets = self.market_store.get_all_markets()
    for market in markets:
      self.update_ground_truth(market.id)
    for trader in self.traders:
      for market in markets:
        trade = await trader.decide_trade(self.ground_truths, market)
        if trade:
          self.market_store.market_bet(
            trade['market_id'],
            trade['is_yes'],
            trade['stake']
          )
        await asyncio.sleep(random.uniform(0.1, 0.5))

  async def run_simulation(self, interval_seconds: float = 5.0):
    self.is_running = True
    while self.is_running:
      await self.run_trading_cycle()
      await asyncio.sleep(interval_seconds)
  
  async def stop_simulation(self):
    self.is_running = False
