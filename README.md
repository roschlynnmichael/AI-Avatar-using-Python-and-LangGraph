# AI Avatar using Python & LangGraph
A real-time, cinematic AI Avatar application built with a Python backend and a Next.js frontend. This project leverages LangGraph for conversational logic, LiveKit for ultra-low latency WebRTC streaming, Cartesia for Text-to-Speech (TTS), and Anam for visual avatar rendering.

To ensure maximum privacy and avoid API timeouts, this project utilizes **Ollama** for local, real-time LLM inference, optimized for lower-VRAM GPUs.

## Features
* **Cinematic Full-Screen UI:** A modern, edge-to-edge video avatar canvas with a glassmorphic (transparent, frosted glass) chat overlay.
* **Local LLM Processing:** Powered by Ollama (recommending `llama3.2:3b` or `qwen2.5:1.5b`) to run entirely on local hardware without API conversation limits.
* **Smart VRAM Warmup:** Synchronous model loading before server initialization to prevent LiveKit heartbeat timeouts.
* **Real-time Lip Sync:** Seamless audio-to-video synchronization powered by Cartesia and Anam.
* **Asynchronous LangGraph:** Thread-offloaded LLM invocations to maintain stable WebRTC connections during heavy compute.

## Tech Stack used
**Backend:**
* Python (3.10 / 3.11 recommended)
* [LangGraph]: Used for conversational routing and building the logic of the AI Avatar
* [Livekit Python SDK]: WebRTC, Building the lifecycle of the agent
* [Cartesia]: TTS Modeling
* [Anam]: Visual Persona Generation
* [Ollama]: Local LLM Host

**Frontend:**
* Next.js / React
* Livekit React Components
* Tailwind CSS (For styling & Glassmorphism)

## Pre-requisites
Before you begin ensure you have the following setup completed
1. Python 3.11 / 3.12
2. Node.Js
3. Ollama (To run LLMs locally on your machine)
4. Environment Variables (Refer to the .env file in the project root)

## Installation
1. Open up a terminal and run 'ollama pull llama3.2:3b'
2. Navigate to project root and create a python virtual environment 'python -m venv venv'
3. Install the pre-requisites from the requirements.txt using 'pip install -r requirements.txt'
4. Create a .env file and add your API Keys
```
# LiveKit Configuration
LIVE_KIT_WEBSOCKET_URL="Your livekit project URL starting in WSS"
LIVE_KIT_API_KEY="Your livekit project API key"
LIVE_KIT_API_SECRET="Your livekit project secret key"

# Deepgram Configuration
DEEPGRAM_API_KEY="Your deepgram api key"

# Cartesia API Configuration
CARTESIA_API_KEY="Your cartesia api key"

# OpenAI API Configuration
OPENAI_API_BASE="Ollama URL (localhost for running it locally on your machine)"
OPENAI_API_KEY="default api key is ollama"

# ANAM Model Configuration
ANAM_AVATAR_ID="Your ANAM Lab Avatar ID"
ANAM_API_KEY="Your ANAM Lab api key"
```

5. Setup the frontend 
```
npm install @livekit/components-react livekit-client
npm install
```

6. Start the backend servers. The frontend needs a random JWT token to be able to talk to livekit
```
python main.py dev
python token_generator.py
```

7. Then start the frontend server using 'npm run dev'

8. Open up a web browser and navigate to 'http://localhost:3000' and click on start conversation.

## Some additional notes
1. Telemetry Bypass: The backend utilizes the official livekit.agents.Agent base class as a dummy variable to pass to bypass internal livekit analytics and prevent program crashes.
2. Thread Offloading: Inside on_data_async, the app.invoke() method is wrapped in asyncio.to_thread() to prevent Python's main event loop from blocking during text generation, which would otherwise cause the LiveKit server to drop the connection.
