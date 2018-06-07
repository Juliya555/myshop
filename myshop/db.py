import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, join, select
)

meta = MetaData()

product = Table(
    'product', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('slug', String(100), nullable=False, unique=True),
    Column('category_id', Integer, ForeignKey('category.id', ondelete='CASCADE')),
    Column('clicks_quantity', Integer, default=0)
)

category = Table(
    'category', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(30), nullable=False),
    Column('slug', String(30), nullable=False, unique=True)
)

product_image = Table(
    'product_image', meta,

    Column('id', Integer, primary_key=True),
    Column('image_filename', String(50)),
    Column('product_id', Integer, ForeignKey('product.id', ondelete='CASCADE'))
)


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def products_api(conn, category_id):
    """Provide list of dictionaries with products of certain category.
    Category_id = 0 - for getting all products)"""
    products_join = join(product, product_image, product.c.id == product_image.c.product_id)
    if category_id > 0:
        query = (select([product.c.id, product.c.name, product.c.slug, product.c.category_id,
                         product.c.clicks_quantity, product_image.c.image_filename])
            .select_from(products_join)
            .where(product.c.category_id == category_id))
    else:
        query = (select([product.c.id, product.c.name, product.c.slug, product.c.category_id,
                         product.c.clicks_quantity, product_image.c.image_filename])
            .select_from(products_join))
    cursor = await conn.execute(query)
    records = await cursor.fetchall()
    return [dict(item) for item in records]


async def save_click(conn, product_id):
    result = await conn.execute(
        product.update()
            .returning(product.c.clicks_quantity)
            .where(product.c.id == product_id)
            .values(clicks_quantity=product.c.clicks_quantity + 1))
    record = await result.fetchone()
    if not record:
        msg = "Product with id {} does not exists"
        raise RecordNotFound(msg.format(product_id))
    return dict(record)
