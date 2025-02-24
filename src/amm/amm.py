from datetime import datetime

from .. import models

'''
AMM base class
'''
class AMM:
  market_id: str
  question: str
  created_at: datetime
  volume: float
  historical_data: list[(datetime, float)]
  probability: float = 0.5
  maxlen = 500
  
  def __init__(self, market_id: str, seed_data: models.MarketSeedData):
    self.market_id = market_id
    self.question = seed_data.question
    self.created_at = datetime.now()
    self.volume = 0.0
    self.historical_data = []

  # Process a trade and return the number of shares purchased
  def process_purchase(self, token: models.Token, stake: float) -> float:
    raise NotImplementedError()
  
  def get_market_info(self) -> models.MarketData:
    return models.MarketData(
      id=self.market_id,
      question=self.question,
      created_at=self.created_at,
      probability=self.probability,
      volume=self.volume,
      history=self.historical_data,
    )

'''
Constant product market maker (like Uniswap):
The invariant condition is: [YES_RESERVES] x [NO_RESERVES] === CONSTANT
'''
class CPMM(AMM):
  yes_reserves: float
  no_reserves: float
  k: float

  def __init__(self, market_id: str, seed_data: models.MarketSeedData):
    super().__init__(market_id, seed_data)
    self.yes_reserves = 100
    self.no_reserves = 100
    self.k = 100 * 100
    self.probability = 0.5
    self.historical_data.append((datetime.now(), 0.5))

  def process_purchase(self, token, stake):
    if stake <= 0:
      raise ValueError('Stake must be positive')
    
    # mint new shares - $[stake] can always be convertes into [stake] YES shares
    # and [stake] NO shares, because these are binomial events
    tmp_yes_reserves = self.yes_reserves + stake
    tmp_no_reserves = self.no_reserves + stake
    
    # calculate number of shares to give to user while keeping invariant
    tokens_purchased = 0
    if token == models.Token.YES:
      tokens_purchased = tmp_yes_reserves - self.k / tmp_no_reserves
      tmp_yes_reserves = self.k / tmp_no_reserves
    else:
      tokens_purchased = tmp_no_reserves - self.k / tmp_yes_reserves
      tmp_no_reserves = self.k / tmp_yes_reserves

    self.yes_reserves = tmp_yes_reserves
    self.no_reserves = tmp_no_reserves
    self.probability = self.no_reserves / (self.yes_reserves + self.no_reserves)
    self.volume += stake
    self.historical_data.append((datetime.now(), self.probability))
    if len(self.historical_data) > self.maxlen:
      self.historical_data = self.historical_data[1:]
    return tokens_purchased
