from typing import Union
from fastapi import FastAPI

from lib import markets

app = FastAPI()
market_store = markets.MarketStore()

@app.get("/markets")
def read_root():
  return market_store.get_all_markets()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
  return { "item_id": item_id, "q": q}
