from fastapi import FastAPI, Depends, HTTPException, Query
from scraper.scraper import Scraper
from scraper.settings import Settings
from scraper.models import ScrapeResponse
import os

app = FastAPI()

settings = Settings()

@app.get("/scrape", response_model=ScrapeResponse)
async def scrape(pages: int = Query(5), proxy: str = Query(None), token: str = Query(None)):
    if token != settings.AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    scraper = Scraper(pages, proxy)
    result = await scraper.scrape()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
