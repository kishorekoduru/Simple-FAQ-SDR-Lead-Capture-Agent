# Simple FAQ SDR + Lead Capture Agent

A voice-based Sales Development Representative (SDR) agent built with LiveKit Agents for Razorpay. This agent can answer FAQ questions and capture lead information through natural conversation.

## 🎯 Day 5 Challenge - Murf AI Voice Agents Challenge

This project implements the **Day 5 Primary Goal** from the Murf AI Voice Agents Challenge:
- ✅ SDR persona for Razorpay (Indian payments company)
- ✅ FAQ-based question answering
- ✅ Natural lead information collection
- ✅ End-of-call summary and data storage

## 🚀 Features

### Core Functionality
- **Voice-based SDR** that represents Razorpay
- **FAQ Answering** using structured company data
- **Lead Capture** - Collects:
  - Name
  - Company Name
  - Email
  - Role/Designation
  - Use Case
  - Team Size
  - Timeline (now/soon/later)
- **Automatic Data Storage** - Saves leads to JSON files

### Technology Stack
- **Backend**: LiveKit Agents (Python)
- **Frontend**: Next.js 15 with TypeScript
- **Voice Services**:
  - Murf AI (Text-to-Speech)
  - Deepgram (Speech-to-Text)
  - Google Gemini 1.5 Flash (LLM)
- **Infrastructure**: LiveKit Cloud

## 📋 Prerequisites

- Python 3.10+ with `uv` package manager
- Node.js 18+ with `pnpm`
- API Keys for:
  - LiveKit Cloud
  - Murf AI
  - Deepgram
  - Google Gemini

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kishorekoduru/Simple-FAQ-SDR-Lead-Capture-Agent.git
cd Simple-FAQ-SDR-Lead-Capture-Agent
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies with uv
uv sync

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
# LIVEKIT_URL=wss://your-livekit-url
# LIVEKIT_API_KEY=your-api-key
# LIVEKIT_API_SECRET=your-api-secret
# GOOGLE_API_KEY=your-gemini-key
# MURF_API_KEY=your-murf-key
# DEEPGRAM_API_KEY=your-deepgram-key
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
pnpm install

# Copy environment template
cp .env.example .env

# Edit .env and add your LiveKit credentials:
# LIVEKIT_URL=wss://your-livekit-url
# LIVEKIT_API_KEY=your-api-key
# LIVEKIT_API_SECRET=your-api-secret
```

### 4. Run the Application

From the root directory:

```bash
bash start_app.sh
```

This will start:
- Backend agent on LiveKit Cloud
- Frontend on http://localhost:3000

## 🎮 Usage

1. Open http://localhost:3000 in your browser
2. Click "Start call"
3. Speak to the agent:
   - Ask about Razorpay: "What does Razorpay do?"
   - Inquire about pricing: "What are your pricing plans?"
   - The agent will naturally collect your information during the conversation
4. Say "That's all" or "I'm done" to end the call
5. The agent will summarize and save your lead data to `lead_<name>.json`

## 📁 Project Structure

```
.
├── backend/
│   ├── src/
│   │   ├── day5_sdr.py        # Main SDR agent implementation
│   │   ├── agent.py           # Original starter agent
│   │   └── minimal_agent.py   # Minimal test agent
│   ├── razorpay_data.json     # FAQ and pricing data
│   └── pyproject.toml         # Python dependencies
├── frontend/
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   └── hooks/                 # Custom React hooks
├── challenges/                # Challenge task descriptions
└── start_app.sh              # Startup script
```

## 🔧 Key Implementation Details

### Fixed Room Name
The frontend uses a consistent room name (`sdr-demo-room`) instead of random names, ensuring the agent can reliably connect to the same room.

### Lead Data Collection
The agent uses LiveKit function tools to collect lead information:
- `update_lead_info()` - Updates lead data as conversation progresses
- `finalize_call()` - Saves lead data when conversation ends

### Company Data
Razorpay FAQ and pricing information is loaded from `razorpay_data.json` and embedded in the agent's instructions for accurate responses.

## 🐛 Troubleshooting

### No Voice Output
1. **Check for zombie processes**: Kill any old agent processes
   ```bash
   pkill -9 -f "day5_sdr.py"
   ```
2. **Verify API keys**: Ensure all API keys in `.env` files are correct
3. **Check browser permissions**: Allow microphone access

### Agent Not Connecting
- Ensure both backend and frontend are running
- Check that LiveKit credentials match in both `.env` files
- Verify the room name is consistent (`sdr-demo-room`)

## 📝 License

This project is licensed under the Apache License 2.0.

## 🙏 Acknowledgments

- Built for the **Murf AI Voice Agents Challenge**
- Powered by **LiveKit Agents**
- Uses **Murf Falcon** for ultra-fast TTS

## 📞 Contact

For questions or issues, please open an issue on GitHub.

---

**#MurfAIVoiceAgentsChallenge** | **#10DaysofAIVoiceAgents**
