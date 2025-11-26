import logging
import json
import os
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    WorkerOptions,
    RoomInputOptions,
    cli,
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("day5_sdr")
load_dotenv(".env")

# Load Razorpay Data
try:
    with open("razorpay_data.json", "r") as f:
        RAZORPAY_DATA = json.load(f)
except FileNotFoundError:
    logger.error("razorpay_data.json not found!")
    RAZORPAY_DATA = {}

class SDRAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=f"""You are a Sales Development Representative (SDR) for Razorpay, India's leading payments solution provider.

Your goals are:
1. Answer questions about Razorpay using the provided FAQ and Pricing information.
2. Qualify the lead by collecting the following information naturally during the conversation:
   - Name
   - Company Name
   - Email
   - Role/Designation
   - Use Case (What do they want to use Razorpay for?)
   - Team Size
   - Timeline (When do they plan to start?)

Company Information:
{json.dumps(RAZORPAY_DATA, indent=2)}

Guidelines:
- Be professional, warm, and helpful.
- Do not make up information. If you don't know, say so.
- Ask for details one by one naturally, don't interrogate.
- When the user says "That's all" or "I'm done", summarize what you collected and use the finalize_call tool.
- Keep responses concise and conversational.
""",
        )
        self.lead_data = {}

    async def save_lead_data(self):
        """Saves the collected lead data to a JSON file."""
        if not self.lead_data:
            logger.warning("No lead data to save")
            return
        
        filename = f"lead_{self.lead_data.get('name', 'unknown').replace(' ', '_')}.json"
        try:
            with open(filename, "w") as f:
                json.dump(self.lead_data, f, indent=2)
            logger.info(f"Lead data saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save lead data: {e}")

    @function_tool
    async def update_lead_info(
        self,
        ctx: RunContext,
        name: str = None,
        company: str = None,
        email: str = None,
        role: str = None,
        use_case: str = None,
        team_size: str = None,
        timeline: str = None,
    ):
        """Updates the lead information with new details provided by the user.
        
        Args:
            name: The name of the user
            company: The company name
            email: The email address
            role: The user's role or designation
            use_case: The intended use case for Razorpay
            team_size: The size of the team
            timeline: Implementation timeline (now/soon/later)
        """
        if name: self.lead_data['name'] = name
        if company: self.lead_data['company'] = company
        if email: self.lead_data['email'] = email
        if role: self.lead_data['role'] = role
        if use_case: self.lead_data['use_case'] = use_case
        if team_size: self.lead_data['team_size'] = team_size
        if timeline: self.lead_data['timeline'] = timeline
        
        logger.info(f"Updated lead data: {self.lead_data}")
        return "Lead information updated successfully."

    @function_tool
    async def finalize_call(self, ctx: RunContext):
        """Call this when the user indicates they are done or wants to end the conversation."""
        await self.save_lead_data()
        return "Call finalized and lead data saved."

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    logger.info(f"Starting SDR agent for room: {ctx.room.name}")
    
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-1.5-flash"),
        tts=murf.TTS(
            voice="en-US-matthew",
            style="Conversation",
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
    )

    agent = SDRAgent()
    
    await session.start(
        agent=agent,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()
    logger.info("SDR agent connected and ready")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
