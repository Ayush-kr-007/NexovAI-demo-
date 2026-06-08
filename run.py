import asyncio
import os
from database import init_db
from main import bot
from pipecat.runner.run import main as pipecat_main

if __name__ == "__main__":
    init_db()

    os.environ["HOST"] = "0.0.0.0"
    os.environ["PORT"] = os.getenv("PORT", "10000")

    # IMPORTANT: ensure bot is discoverable
    os.environ["PIPECAT_BOT"] = "main:bot"

    asyncio.run(pipecat_main())