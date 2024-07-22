import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import os
from .models import Product, ScrapeResponse

class Scraper:
    def __init__(self, pages: int, proxy: str = None):
        self.pages = pages
        self.proxy = proxy
        self.base_url = "https://dentalstall.com/shop/page/"
        self.products = []
        self.cache = {}

    async def fetch_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def scrape_page(self, session, page_num):
        url = f"{self.base_url}{page_num}/"
        try:
            html = await self.fetch_page(session, url)
            soup = BeautifulSoup(html, 'html.parser')
            for item in soup.select('.product'):
                title = item.select_one('.woocommerce-loop-product__title').get_text(strip=True)
                price = item.select_one('.woocommerce-Price-amount').get_text(strip=True)
                img_url = item.select_one('img').get('src')
                img_path = await self.download_image(img_url)
                product = Product(product_title=title, product_price=float(price.replace('$', '').replace(',', '')), path_to_image=img_path)
                if self.is_product_updated(product):
                    self.products.append(product)
        except Exception as e:
            print(f"Error scraping page {page_num}: {e}")

    async def download_image(self, url):
        filename = os.path.basename(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(filename, 'wb') as f:
                        f.write(await resp.read())
                    return os.path.abspath(filename)
        return ""

    def is_product_updated(self, product):
        # Implement caching and comparison logic
        if product.product_title in self.cache:
            if self.cache[product.product_title].product_price == product.product_price:
                return False
        self.cache[product.product_title] = product
        return True

    async def scrape(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.scrape_page(session, i) for i in range(1, self.pages + 1)]
            await asyncio.gather(*tasks)
        self.save_to_db()
        return ScrapeResponse(total_products=len(self.products), products=self.products)

    def save_to_db(self):
        with open('scraped_data.json', 'w') as f:
            json.dump([product.dict() for product in self.products], f, indent=4)
        print(f"Scraped {len(self.products)} products and saved to DB.")
