import asyncio
import os
from database import init_db
from cat_pipe import bot
from pipecat.runner.run import main as pipecat_main

if __name__ == "__main__":
    init_db()

    os.environ["HOST"] = "0.0.0.0"
    os.environ["PORT"] = os.getenv("PORT", "10000")

    # IMPORTANT: ensure bot is discoverable
    os.environ["PIPECAT_BOT"] = "cat_pipe:bot"

    asyncio.run(pipecat_main())