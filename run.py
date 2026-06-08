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

# import sys # 👈 Import sys at the top of your script block

# if __name__ == "__main__":
#     init_db()

#     # Get the dynamic port assigned by Railway, defaulting to 7860
#     port = os.getenv("PORT", "7860")

#     # 🚀 CRITICAL FIX: Inject CLI flags directly into sys.argv
#     # This forces Pipecat's internal Uvicorn server to bind correctly.
#     sys.argv.extend(["--host", "0.0.0.0", "--port", port])

#     # IMPORTANT: ensure bot is discoverable
#     os.environ["PIPECAT_BOT"] = "main:bot"

#     asyncio.run(pipecat_main())
