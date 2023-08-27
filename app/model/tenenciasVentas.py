from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import String,DATE,FLOAT
from app.config.db import meta, engine




tenenciasVentas = Table(
    "tenenciasVentas",
    meta,
    Column("ticker", String(50)),
    Column("tipoInstrumento", String(50)),
    Column("fecha",DATE),
    Column("precio", FLOAT),
    Column("cantidad", FLOAT),
    Column("moneda", String(50)),
    Column("comision", FLOAT)
)

meta.create_all(engine)



