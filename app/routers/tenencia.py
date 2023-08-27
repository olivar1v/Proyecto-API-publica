from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from sqlalchemy import select, func

from app.model.tenenciasCompras import tenenciasCompras
from app.model.tenenciasVentas import tenenciasVentas
from app.model.dividendos import dividendos
from app.config.db import conn



router = APIRouter(prefix="/Tenencias",tags=["Tenencias"] )

class Tenencia(BaseModel):
    ticker: str
    tipoInstrumento: str
    tipoMoneda:str
    fecha: date
    precio: float
    cantidad: float
    comision: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "BTCUSDT/C/YPFD",
                    "tipoInstrumento": "CRIPTO/CEDEAR/MERVAL",
                    "tipoMoneda": "USDT/USD/PESO/",
                    "fecha": "2023-12-31",
                    "precio": 35.4,
                    "cantidad": 3.2,
                    "comision": 22.32
                }
            ]
        }
    }
    


class Dividendo(BaseModel):
    ticker: str
    fecha: date
    total: float
    moneda: str
    


@router.post("/compra")
async def comprar_posicion(tenenciaCompra: Tenencia):
    conn.execute(tenenciasCompras.insert().values( {"fecha":tenenciaCompra.fecha,"ticker":tenenciaCompra.ticker,"precio":tenenciaCompra.precio,"cantidad":tenenciaCompra.cantidad,"moneda":tenenciaCompra.tipoMoneda,"comision":tenenciaCompra.comision,"tipoInstrumento":tenenciaCompra.tipoInstrumento}))
    conn.commit()
    return {"message":"compra agregada"}



@router.post("/venta")
async def vender_posicion(tenenciaVenta: Tenencia):
    cantVenta = conn.execute(select(func.coalesce(func.sum(tenenciasVentas.c.cantidad),0).label("suma")).where(tenenciasVentas.c.ticker== tenenciaVenta.ticker))
    cantCompra = conn.execute(select(func.coalesce(func.sum(tenenciasCompras.c.cantidad),0).label("suma")).where(tenenciasCompras.c.ticker == tenenciaVenta.ticker))
    conn.commit()

    cantCompra = [dict(r._mapping) for r in cantCompra]
    cantVenta = [dict(r._mapping) for r in cantVenta]

    cantTotal = cantCompra[0]["suma"]-cantVenta[0]["suma"]
    if cantTotal>= tenenciaVenta.cantidad and cantCompra[0]["suma"]!= 0 :
        conn.execute(tenenciasVentas.insert().values( {"fecha":tenenciaVenta.fecha,"ticker":tenenciaVenta.ticker,"precio":tenenciaVenta.precio,"cantidad":tenenciaVenta.cantidad,"moneda":tenenciaVenta.tipoMoneda,"comision":tenenciaVenta.comision,"tipoInstrumento":tenenciaVenta.tipoInstrumento}))
        conn.commit()
        return {"message":"venta agregada"}
    return {"message": "la cantidad ingresada supera la actual"}



@router.post("/dividendos")
async def agregar_dividendo(dividendo:Dividendo):
    conn.execute(dividendos.insert().values( {"fecha":dividendo.fecha,"ticker":dividendo.ticker,"total":dividendo.total,"moneda":dividendo.moneda}))
    conn.commit()
    return {"message":"compra agregada"}





    
