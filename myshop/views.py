from aiohttp import web
import aiohttp_jinja2

import db


async def get_products(request):
    async with request.app['db'].acquire() as conn:
        category_id = int(request.match_info['category_id'])
        products_for_api = await db.products_api(conn, category_id)
        return web.json_response({'products': products_for_api})


async def click_product(request):
    async with request.app['db'].acquire() as conn:
        product_id = int(request.match_info['product_id'])
        clicks_now = await db.save_click(conn, product_id)
        return web.json_response(clicks_now)


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@aiohttp_jinja2.template('products.html')
async def products(request):
    async with request.app['db'].acquire() as conn:
        categories_cursor = await conn.execute(db.category.select())
        categories_records = await categories_cursor.fetchall()
        categories = [dict(q) for q in categories_records]
        return {'categories': categories}
