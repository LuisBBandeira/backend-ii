from fastapi import FastAPI
import asyncio
from datetime import datetime
import random

app = FastAPI()

async def fetch_data_from_source_1():
    delay = random.uniform(0.5, 1.5)
    await asyncio.sleep(delay)
    
    return {
        "source": "Source 1",
        "data": {"value": 42, "description": "The answer to everything"},
        "timestamp": datetime.now().isoformat(),
        "delay": f"{delay:.2f} seconds"
    }

async def fetch_data_from_source_2():
    delay = random.uniform(0.5, 1.5)
    await asyncio.sleep(delay)
    
    return {
        "source": "Source 2",
        "data": {"items": ["alpha", "beta", "delta"], "count": 3},
        "timestamp": datetime.now().isoformat(),
        "delay": f"{delay:.2f} seconds"
    }

@app.get("/fetch-data")
async def fetch_data():
    source1_data, source2_data = await asyncio.gather(
        fetch_data_from_source_1(),
        fetch_data_from_source_2()
    )
    
    return {
        "message": "Data fetched concurrently from both sources",
        "source1": source1_data,
        "source2": source2_data,
        "total_time": max(float(source1_data["delay"].split()[0]), 
                        float(source2_data["delay"].split()[0]))
    }