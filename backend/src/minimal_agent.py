import logging
from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
)
from livekit.plugins import google, deepgram, silero

load_dotenv(".env")
logger = logging.getLogger("minimal_agent")

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    logger.info(f"Connecting to room: {ctx.room.name}")
    
    await ctx.connect()
    logger.info("Connected to room")

    agent = Agent()
    
    # Simple session without complex pipeline first, just to see if we can connect
    # But to speak, we need TTS.
    session = AgentSession(
        stt=deepgram.STT(),
        llm=google.LLM(model="gemini-1.5-flash"),
        tts=google.TTS(voice="en-US-Standard-C"),
        vad=ctx.proc.userdata["vad"],
    )
    
    @session.on("agent_started_speaking")
    def on_speak(ev):
        logger.info("Agent started speaking")
    
    await session.start(agent=agent, room=ctx.room)
    
    logger.info("Session started. Attempting to say hello...")
    await session.say("Hello. This is a test.", text_pacing=True)
    logger.info("Say command issued.")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
