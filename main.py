import asyncio

# Load environment variables from .env file 
from dotenv import load_dotenv

# Import necessary modules from the LiveKit agents framework
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant

# Import plugins for voice activity detection (VAD), speech-to-text (STT), and text-to-speech (TTS)
from livekit.plugins import cartesia, deepgram, silero

# Import the custom AssistantFnc class from the api module
from api import AssistantFnc


# Load environment variables from a .env file
load_dotenv()


# Import Groq LLM (Language Learning Model) from the OpenAI plugin
from livekit.plugins.openai import llm as openai_llm 

# Configure the Groq LLM with specific parameters
groq_llm = openai_llm.LLM.with_groq(
  model="llama3-8b-8192",# Specify the model to use
  temperature=0.8,# Set the temperature for creativity in responses
)


# Create an instance of the AssistantFnc class to handle custom functions
fnc_ctx = AssistantFnc()


# Define the entrypoint function for the voice assistant
async def entrypoint(ctx: JobContext):## This is the function called by WorkerOption down bellow
    """
    This function is called when the worker starts. It sets up the voice assistant and connects it to a LiveKit room.
    """
    # Create an initial context for the LLM to guide its behavior
    initial_ctx = llm.ChatContext().append( 
        role="system",
        text=(
            "You are a Library Voice Assistant."
            "You will help user in book recommendations, reservations and returns."
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
        ),
    )
    # Connect to the LiveKit room, subscribing only to audio (no video)
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Create a VoiceAssistant instance with the following components:
    assitant = VoiceAssistant(
        vad=silero.VAD.load(),#Voice Activity Detection to detect if the user is speaking or not so we know when to cut them off
        stt=deepgram.STT(),# Speech-to-Text model to convert user speech into text. Deepgram has Free API access with limited usage.
        llm=groq_llm,## Select the type of LLM  
        tts=cartesia.TTS(),# Text-to-Speech model to convert text into speech. Cartesia has Free API access with limited usage.
        chat_ctx=initial_ctx,# Provide the initial context to the LLM
        fnc_ctx=fnc_ctx,  # Provide the custom function context for handling specific tasks
        max_nested_fnc_calls=4, # Limit the number of nested function calls, had some error because the nested function called were not sufficient in the past
    )

    # Start the assistant in the LiveKit room
    assitant.start(ctx.room)#connect to a "room"

    ##voice assistant can connect to one or many "room". Here we are telling the "ctx:JobContext" to connect to the room
    ##The agent is gonna connect to the liveKit Server
    ##The liveKit Server is gonna send the agent a job
    ## When that Job is sent, it's gonna have a riim associated with it


    # Wait for 1 second to ensure everything is initialized
    await asyncio.sleep(1)

    # The assistant first message by greeting the user with a welcome message
    await assitant.say("Welcome to the library center, how can I help you today!", allow_interruptions=True)


# Run the application if this script is executed directly
if __name__ == "__main__":
    # Use the LiveKit CLI to run the app with the specified entrypoint function
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))