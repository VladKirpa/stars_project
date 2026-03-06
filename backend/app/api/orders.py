from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
import asyncio
from app.schemas.order import OrderCreate, OrderRead
from app.orm.orders_orm import create_order, get_created_orders
from app.database import get_db


router = APIRouter()


@router.post('/create-order', response_model=OrderRead)
async def create_order_endpoint(order_data: OrderCreate, session= Depends(get_db)):
    
    try:
        order_create = await create_order(order_data, session)
        return order_create
    except Exception as e:
        print(f"Error : {e}")
        raise HTTPException(500, detail=str(e))
        



@router.get('/get-my-order/{tg_id}', response_model=list[OrderRead])
async def get_created_order_enpoint(tg_id: int, session=Depends(get_db)): # Return order for creator in menu
    try:
        data = await get_created_orders(tg_id, session)
        return data
    except Exception as e:
        print(f"Error : {e}")
        raise HTTPException(500, detail=str(e))
    


