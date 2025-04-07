from fastapi import FastAPI
import asyncio

app = FastAPI()

async def simulated_io_task():
    await asyncio.sleep(1)
    return "Data fetched!"

@app.get("/async-data")
async def get_data():
    result = await simulated_io_task()
    return {"message": result}