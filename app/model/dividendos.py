from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import String,DATE,FLOAT
from app.config.db import meta, engine




dividendos = Table(
    "dividendos",
    meta,
    Column("ticker", String(50)),
    Column("fecha",DATE),
    Column("total", FLOAT),
    Column("moneda", String(50))
)

meta.create_all(engine)


