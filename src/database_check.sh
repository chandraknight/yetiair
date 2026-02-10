#!/bin/bash
# Check if database is reachable

# You might need to install postgresql-client or similar tools
# or use a python script to check connection if preferred.
# For now, using a simple python check using the generic db module.

python3 -c "
import asyncio
from src.db import engine

async def check():
    try:
        async with engine.connect() as conn:
            print('Database connected successfully.')
    except Exception as e:
        print(f'Database connection failed: {e}')
        exit(1)

asyncio.run(check())
"
