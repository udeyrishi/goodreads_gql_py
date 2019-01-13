from aiodataloader import DataLoader
import asyncio

def data_loaded(fn, loop):
    async def batch_load_fn(keys):
        tasks = [asyncio.create_task(fn(id)) for id in keys]
        return [await task for task in tasks]
    
    return DataLoader(batch_load_fn=batch_load_fn, loop=loop)