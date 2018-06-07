from views import index, products, get_products, click_product
from settings import BASE_DIR


def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/products', products, name='products')
    app.router.add_get('/api/products/{category_id}', get_products)
    app.router.add_post('/api/click_product/{product_id}', click_product)
    app.router.add_static('/static',
                          path=BASE_DIR / 'myshop/static',
                          name='static')
