import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import cartesia, deepgram, silero



# Import Groq LLM
from livekit.plugins.openai import llm as openai_llm 

# Configure Groq LLM
groq_llm = openai_llm.LLM.with_groq(
  model="llama3-8b-8192",
  temperature=0.8,
)

load_dotenv()


async def entrypoint(ctx: JobContext):## This is the function called by WorkerOption down bellow
    initial_ctx = llm.ChatContext().append( ##this part give context to the LLM
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice.You are build with Llama3 "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY) ## Specify that we want to connect to the Audio

    assitant = VoiceAssistant(##define the characteristic of the voice assistant,
        vad=silero.VAD.load(),##Voice Activity Detection to detect if the user is speaking or not so we know when to cut them off
        stt=deepgram.STT(),## Speech to text (could use something else)
        llm=groq_llm,## Select the type of LMM  
        tts=cartesia.TTS(),## Text to speech model (could be use another one)
        chat_ctx=initial_ctx,## give the initial context defined in the async function
       
    )
    # Start the assistant in the room
    assitant.start(ctx.room)##connect to a "room"

    ##voice assistant can connect to one or many "room". Here we are telling the "ctx:JobContext" to connect to the room
    ##The agent is gonna connect to the liveKit Server
    ##The liveKit Server is gonna send the agent a job
    ## When that Job is sent, it's gonna have a riim associated with it

    await asyncio.sleep(1)## This ask the agent to wait 1 sec
    await assitant.say("Hello, how can I help you today!", allow_interruptions=True) ## first thing the assistant will say.


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

