from fastapi import HTTPException, APIRouter
from tortoise.transactions import in_transaction
from src.models import EnrichedStocks
from src.celery import celery_client
import time


router = APIRouter(
    prefix='/stock',
    tags=['stock']
)

@router.post("/{symbol}")
async def create_stock_entry(symbol: str):
    task_data = {
        "process_name": "enrich_stock",
        "data": symbol
    }
    # Submit the Celery task
    task = celery_client.send_task("handle_task", args=[task_data])
    task_id = task.id

    # Poll for the task result
    max_retries = 30 
    sleep_interval = 2

    for _ in range(max_retries):
        task_result = celery_client.AsyncResult(task_id)

        if task_result.state == "PENDING":
            time.sleep(sleep_interval)
            continue
        elif task_result.state == "FAILURE":
            raise HTTPException(status_code=500, detail="Failed to enrich stock data.")
        elif task_result.state == "SUCCESS":
            stock_data = task_result.result
            async with in_transaction():
                # Save to database
                await EnrichedStocks.create(**stock_data)
            return {"message": "Stock entry created successfully", "data": stock_data}

    raise HTTPException(status_code=408, detail="Task timed out")


@router.get("/")
async def get_stock_entry():
    stocks = await EnrichedStocks.all()
    return stocks


@router.put("/{symbol}")
async def update_stock_entry(symbol: str, updated_data: dict):
    stock = await EnrichedStocks.get_or_none(symbol=symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    for key, value in updated_data.items():
        setattr(stock, key, value)
    await stock.save()
    return {"message": "Stock updated successfully", "data": updated_data}


@router.delete("/{symbol}")
async def delete_stock_entry(symbol: str):
    stock = await EnrichedStocks.get_or_none(symbol=symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    await stock.delete()
    return {"message": "Stock deleted successfully"}
