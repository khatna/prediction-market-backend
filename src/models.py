import enum
from pydantic import BaseModel
from typing import List, Tuple
from datetime import datetime

class MarketData(BaseModel):
  id: str
  question: str
  created_at: datetime
  probability: float
  volume: float
  history: List[Tuple[datetime, float]]

class MarketSeedData(BaseModel):
  question: str
  initial_probability: float

class Bet(BaseModel):
  market_id: str
  is_yes: bool # True for buy, false for sell
  stake: float
  
class BetResponse(BaseModel):
  purchased: float
  market_data: MarketData

class Token(enum.Enum):
  YES = 1
  NO = 2

