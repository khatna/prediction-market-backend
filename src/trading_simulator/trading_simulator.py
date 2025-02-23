import asyncio
import random
from dataclasses import dataclass

@dataclass
class SimulatedTrader:
  name: str
  bias: float  # Tendency to bet yes (0-1)
  activity_level: float  # Probability they decide to trade
  
  async def decide_trade(self, market_data):
    if random.random() > self.activity_level:
      return None
            
    implied_probability = market_data.probability
    is_yes = self.bias > implied_probability
    stake = round(random.uniform(5, 20), 2)
    
    return {
        'market_id': market_data.id,
        'is_yes': is_yes,
        'stake': stake
    }

class TradingSimulator:
  def __init__(self, market_store):
    self.market_store = market_store
    self.traders = [
      SimulatedTrader("Optimist", bias=0.7, activity_level=0.3),
      SimulatedTrader("Pessimist", bias=0.3, activity_level=0.3),
      SimulatedTrader("Balanced", bias=0.5, activity_level=0.5),
      SimulatedTrader("FrequentTrader", bias=0.5, activity_level=0.8),
    ]
    self.is_running = False
  
  async def run_trading_cycle(self):
    markets = self.market_store.get_all_markets()
    for trader in self.traders:
      for market in markets:
        trade = await trader.decide_trade(market)
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
