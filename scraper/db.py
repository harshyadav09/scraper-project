import aiomysql
from .settings import Settings

class Database:
    def __init__(self):
        self.settings = Settings()

    async def get_connection(self):
        return await aiomysql.connect(
            host=self.settings.DB_HOST,
            port=self.settings.DB_PORT,
            user=self.settings.DB_USER,
            password=self.settings.DB_PASSWORD,
            db=self.settings.DB_NAME
        )

    async def save_products(self, products):
        conn = await self.get_connection()
        async with conn.cursor() as cursor:
            for product in products:
                await cursor.execute("""
                    INSERT INTO products (product_title, product_price, path_to_image)
                    VALUES (%s, %s, %s)
                """, (product.product_title, product.product_price, product.path_to_image))
        await conn.commit()
        conn.close()
