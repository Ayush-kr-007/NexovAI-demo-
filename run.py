import os
import sys

from database import init_db
from pipecat.runner.run import main as pipecat_main

if __name__ == "__main__":
    init_db()

    port = os.getenv("PORT", "10000")

    sys.argv.extend([
        "--host", "0.0.0.0",
        "--port", port
    ])

    os.environ["PIPECAT_BOT"] = "main:bot"

    pipecat_main()