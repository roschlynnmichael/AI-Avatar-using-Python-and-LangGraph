import asyncio
import json
import os
from livekit import rtc
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from livekit.agents import (
    JobContext, 
    WorkerOptions, 
    cli, 
    voice,
    Agent
)
from livekit.agents.utils import aio
from livekit.plugins import cartesia, anam
from graph import app

load_dotenv(".env")

def warmup_ollama():
    print("-> Pushing Ollama model into VRAM... please wait.")
    try:
        app.invoke(
            {
                "messages": [HumanMessage(content="System initialization. Reply 'ok'.")],
                "mood": "neutral",
                "avatar_animation": "talk_standard",
                "final_text": ""
            }
        )
        print("-> Ollama successfully loaded into VRAM and is ready.")
    except Exception as e:
        print(f"-> Warning during Ollama warmup: {e}")

async def entrypoint(ctx: JobContext):
    avatar = anam.AvatarSession(
        persona_config=anam.PersonaConfig(
            name="Liv",
            avatarId=os.getenv("ANAM_AVATAR_ID"),
        ),
        api_key=os.getenv("ANAM_API_KEY"),
    )

    tts = cartesia.TTS(
        model="sonic-3.5",
        voice="db6b0ed5-d5d3-463d-ae85-518a07d3c2b4"
    )

    session = voice.AgentSession(tts=tts)

    await avatar.start(session, room=ctx.room)
    await ctx.connect()
    
    print(f"-> Liv is connected to room: {ctx.room.name}")

    dummy_agent = Agent(instructions="Custom LangGraph agent override")
    await session.start(room=ctx.room, agent=dummy_agent)

    @ctx.room.on("data_received")
    def on_data(data_packet: rtc.DataPacket):
        if data_packet.topic == "lk-chat-topic":
            asyncio.create_task(on_data_async(data_packet))

    async def on_data_async(data_packet: rtc.DataPacket):
        try:
            payload = data_packet.data.decode("utf-8")
            user_message = json.loads(payload).get("message", payload)
            
            print(f"User sent: {user_message}")
            
            result = await asyncio.to_thread(
                app.invoke,
                {
                    "messages": [HumanMessage(content=user_message)],
                    "mood": "neutral",
                    "avatar_animation": "talk_standard",
                    "final_text": ""
                }
            )
            
            await ctx.room.local_participant.publish_data(
                json.dumps({"animation": result.get('avatar_animation', 'talk_standard')}).encode(),
                topic="avatar-control"
            )
            
            final_text = result.get('final_text', '')
            if final_text:
                await session.say(final_text)
            else:
                print("Warning: Graph returned empty final_text")
                
        except Exception as e:
            print(f"Error in backend logic: {e}")

if __name__ == "__main__":
    warmup_ollama()

    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            ws_url=os.getenv("LIVE_KIT_WEBSOCKET_URL"),
            api_key=os.getenv("LIVE_KIT_API_KEY"),
            api_secret=os.getenv("LIVE_KIT_API_SECRET"),
        )
    )