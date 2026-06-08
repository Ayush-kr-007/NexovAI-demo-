import os
from dotenv import load_dotenv
from loguru import logger
import asyncio

from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.pipeline.worker import PipelineWorker
from pipecat.workers.runner import WorkerRunner
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.sarvam.stt import SarvamSTTService
from pipecat.services.sarvam.tts import SarvamTTSService
from pipecat.services.groq.llm import GroqLLMService
from pipecat.transports.base_transport import TransportParams
from lead_extractor import extract_lead
from lead_manager import save_lead, calculate_score

load_dotenv(override=True)

from database import init_db, save_lead_to_db


async def bot(runner_args: RunnerArguments):
    transport = await create_transport(
        runner_args,
        {
            "webrtc": lambda: TransportParams(
                audio_in_enabled=True,
                audio_out_enabled=True,
                audio_out_sample_rate=16000,
                audio_out_channels=1,
            ),
        },
    )

    stt = SarvamSTTService(
        api_key=os.getenv("SARVAM_API_KEY"),
        settings=SarvamSTTService.Settings(model="saaras:v3"),
    )

    tts = SarvamTTSService(
        api_key=os.getenv("SARVAM_API_KEY"),
        settings=SarvamTTSService.Settings(model="bulbul:v3", voice="shubh"),
    )

    llm = GroqLLMService(
        api_key=os.getenv("GROQ_API_KEY"),
        settings=GroqLLMService.Settings(model="llama-3.3-70b-versatile"),
    )

    messages = [
        {
            "role": "system",
            "content": """You are NexovAI's AI Sales Caller.
Your goal is to qualify potential leads for AI calling automation.
Start by saying: "Hello, this is NexovAI. We help businesses automate customer calls using AI. Is this a good time for a quick 2 minute conversation?"
If YES or MAYBE: Ask qualification questions one at a time.
If NO: Thank them and end the call.
QUALIFICATION QUESTIONS (ask ONE at a time, wait for answer):
1. How are customer calls currently handled in your business?
2. Approximately how many customer calls do you receive daily?
3. What industry are you in?
4. Are you actively exploring AI calling solutions?
5. What budget range are you considering?
6. When would you like to implement a solution?
After all questions, thank the customer and say goodbye.
DO NOT continue the conversation after goodbye.
IMPORTANT:

Do not move to the next question until the current question
has been answered clearly.

If the answer is vague, irrelevant, or unclear,
ask again.

Examples:

Question:
How many calls do you receive daily?

Invalid:
- okay
- maybe
- not sure

Valid:
- 20
- around 50
- 100+

Question:
What budget are you considering?

Invalid:
- yes
- maybe
- okay

Valid:
- 10k
- 20,000
- 1 lakh

After all questions are completed:
Thank the customer and end the conversation.

If the customer says bye or goodbye,
do not respond.
If the customer says goodbye,bye or any words of farewell., do not respond.
RULES: One question at a time. Replies under 20 words. Sound professional. After all questions, thank the customer and say goodbye."""
        }
    ]

    context = LLMContext(messages)
    context_aggregator = LLMContextAggregatorPair(context)
    call_completed = False
    def conversation_finished():
        assistant_msgs = [
            msg["content"]
            for msg in context.messages
            if msg.get("role") == "assistant"
        ]

        if not assistant_msgs:
            return False

        return "thank you, goodbye" in assistant_msgs[-1].lower()
    pipeline = Pipeline([
        transport.input(),
        stt,
        context_aggregator.user(),
        llm,
        tts,
        transport.output(),
        context_aggregator.assistant(),
    ])

    # ✅ Only ONE task, ONE runner
    task = PipelineWorker(pipeline)

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):

        logger.success(
            f"📞 Client connected: {client}"
        )

        await asyncio.sleep(2)
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):

        logger.warning(
            f"📴 Client disconnected: {client}"
        )

        nonlocal call_completed

        if not call_completed:
            call_completed = True
            await task.cancel()
    @task.event_handler("on_pipeline_finished")
    async def on_pipeline_finished(worker, reason=None):
        logger.info("Pipeline finished - extracting lead")
        try:
            conversation = ""
            for msg in context.messages:
                role = msg.get("role")
                if role in ["user", "assistant"]:
                    content = msg.get("content", "")
                    if content:
                        conversation += f"{role}: {content}\n"

            print("\n========== CONVERSATION ==========")
            print(conversation if conversation else "(no conversation recorded)")
            print("==================================")

            if not conversation.strip():
                print("No conversation to extract lead from.")
                return

            lead = extract_lead(conversation)
            score, lead_type = calculate_score(
                lead.get("interest", ""),
                lead.get("budget", ""),
                lead.get("timeline", "")
            )
            lead["score"] = score
            lead["lead_type"] = lead_type
            save_lead_to_db(lead)
            print("\nLead Saved:")
            print(lead)
        except Exception as e:
            print("Lead extraction failed:", e)
            

    # ✅ runner.run() is at the TOP LEVEL of bot(), not inside any handler
    runner = WorkerRunner()
    await runner.add_workers(task)
    await runner.run()

if __name__ == "__main__":
    init_db()

    from pipecat.runner.run import main
    main()

# if __name__ == "__main__":
#     from pipecat.runner.run import main
#     main()