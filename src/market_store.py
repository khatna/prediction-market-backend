from typing import Optional, Dict, List
import uuid

from . import models
from .amm import amm

class MarketStore:
  def __init__(self):
    self._markets: Dict[str, amm.AMM] = {}

  def get_all_markets(self) -> List[models.MarketData]:
    return [amm.get_market_info() for amm in list(self._markets.values())]
    
  def get_market(self, market_id: str) -> Optional[models.MarketData]:
    amm = self._markets.get(market_id)
    if amm != None:
      return amm.get_market_info()
  
  def create_market(self, seed_market_data: models.MarketSeedData):
    market_id = str(uuid.uuid4())
    new_market = amm.CPMM(market_id, seed_market_data)
    self._markets[market_id] = new_market

  def market_bet(self, market_id: str, is_yes: bool, stake: float):
    amm = self._markets.get(market_id)
    if not amm:
      raise Exception('Market not found')
    
    token = models.Token.YES if is_yes else models.Token.NO
    return amm.process_purchase(token, stake)
