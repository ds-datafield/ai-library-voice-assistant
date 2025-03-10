# <ins>**AI Library Voice Assistant**</ins>

## **Overview**
The **AI Library Voice Assistant** is a **voice-enabled AI agent** designed to assist users in managing library-related tasks. It leverages **natural language processing (NLP)** and **speech-to-text/text-to-speech technologies** to provide an intuitive and hands-free experience for library users. Whether you're looking for **book recommendations**, checking **availability**, or **reserving** a book, this assistant makes library interactions **seamless** and **efficient**.

This project is built using **Python**, **SQLite** for **database management**, and integrates with **LiveKit** for **real-time voice communication**. It leverages **advanced language models (LLMs)** like **Groq's LLaMA 3** for generating **intelligent** and **context-aware responses**. For **voice interactions**, the assistant utilizes **APIs** such as **Cartesia** for **Text-to-Speech (TTS)**, **Deepgram** for **Speech-to-Text (STT)**, and **Groq** for **natural language understanding** and **processing**.

<ins>*Note</ins>: The current interface for interacting with the **AI Library Voice Assistant** is the [LiveKit Playground](https://agents-playground.livekit.io/), which provides a simple and effective way to test **real-time voice communication**. While this serves as a great starting point, future iterations of the project may include a **custom frontend** for a more tailored and **user-friendly experience**.*

## **Project Demo**
Watch the demo of the **AI Library Voice Assistant**:

[Demo Video](https://www.linkedin.com/posts/davis-se-ly-2b6a3417a_first-look-at-my-ai-powered-library-voice-activity-7304908712069001216-Bl6u?utm_source=share&utm_medium=member_desktop&rcm=ACoAACqC56oBnexbXb9s-w71Pzn4axDQUekmZ6g)

## **Goal**
The primary aim of this project is to explore and experiment with **modern tools** and **technologies** in the **AI** and **voice communication** space, rather than to create a fully fleshed-out **production-ready application**. Specifically, this project serves as a **learning platform** to:

- <ins>**Investigate LiveKit Toolkits**</ins>: Understand and utilize **LiveKit's real-time communication capabilities** for **voice interactions**.
- <ins>**Use Large Language Models (LLMs)**</ins>: Experiment with **large language models** like **Groq's LLaMA 3** to generate **intelligent** and **context-aware responses**.
- <ins>**Interact with Existing AI APIs**</ins>: Gain hands-on experience with **APIs** like **Cartesia (Text-to-Speech)**, **Deepgram (Speech-to-Text)**, and **Groq (LLM for natural language processing)**.
- <ins>**Create a Custom API**</ins>: Develop a simple **API** to handle **library-related tasks**, such as **book lookups**, **reservations**, and **recommendations**.
- <ins>**Build a Small Database**</ins>: Design and implement a lightweight **SQLite database** to manage **library data**.
- <ins>**Leverage Free Credits**</ins>: Utilize **free credits** provided by the tools (e.g., **Deepgram**, **Cartesia**) to build and test the project without incurring costs.

By focusing on these goals, the project provides a **practical way** to explore **cutting-edge technologies** while keeping the scope **manageable** and **cost-effective**.

## **Problem It Solves**
Managing **library resources** can be time-consuming and cumbersome, especially for users who prefer **quick** and **easy access** to information. Traditional library systems often require **manual searches**, **physical visits**, or navigating **complex online interfaces**. The **AI Library Voice Assistant** addresses these challenges by:

- Providing **instant access** to library information through **voice commands**.
- Automating **repetitive tasks** like **book lookups**, **reservations**, and **returns**.
- Offering **personalized book recommendations** based on user preferences.
- Making library services more **accessible** to users with **disabilities** or those who prefer **voice interactions**.

## **Features**
The **AI Library Voice Assistant** can perform the following tasks:

### 1. **Book Lookup**
- Search for books by **title**.
- Retrieve **detailed information** about a book, including its **title**, **author**, **genre**, and **availability**.

### 2. **Book Availability Check**
- Check if a specific book is **available** in the library.
- Provide **real-time updates** on book availability.

### 3. **Book Reservation**
- Reserve a book if it’s **available**.
- Notify the user if the book is already **reserved**.

### 4. **Book Return**
- Facilitate the **return** of a reserved book.
- Update the **library database** to mark the book as **available**.

### 5. **Book Recommendations**
- Recommend books based on **genre**.
- Provide a list of **available books** in a specific category.

### 6. **Voice Interaction**
- Communicate with users through **natural language voice interactions**.
- Use **speech-to-text** and **text-to-speech technologies** for **seamless communication**.

## **How It Works**
1. **Voice Input**: The user interacts with the assistant using **voice commands**.
2. **Speech-to-Text**: The assistant converts the user's speech into **text** using **Deepgram's STT (Speech-to-Text)** technology.
3. **Natural Language Processing**: The assistant processes the text input using **Groq's LLaMA 3** language model to understand the user's **intent**.
4. **Database Query**: The assistant queries the **SQLite database** to retrieve or update **book information**.
5. **Text-to-Speech**: The assistant converts its response into **speech** using **Cartesia's TTS (Text-to-Speech)** technology and communicates it back to the user.

## **Getting Started**
### **Prerequisites**
- **Python**
- **SQLite**
- **LiveKit API key**
- **Groq API key** (for **LLaMA 3**)
- **Deepgram API key** (for **STT**)
- **Cartesia API key** (for **TTS**)

### **Set up the environment** by copying `.env.example` to `.env` and filling in the required values:

```plaintext
LIVEKIT_URL="your_livekit_url_here"
LIVEKIT_API_KEY="your_livekit_api_key_here"
LIVEKIT_API_SECRET="your_livekit_api_secret_here"
GROQ_API_KEY="your_groq_api_key_here"
CARTESIA_API_KEY="your_cartesia_api_key_here"
DEEPGRAM_API_KEY="your_deepgram_api_key_here"
```
### Populate the database with your own book
with create_book() from db_library fill up your own SQL database

### Run the script
Run the agent:

```python main.py dev```


## Acknowledgments
- This project was inspired by the TechWithTim YouTube channel. Special thanks to Tim for his insightful tutorials, which provided the foundation for this project. While this implementation is adapted to my specific use case (an AI Library Voice Assistant), the core concepts and tools were learned from his content. [Link for the tutorial](https://www.youtube.com/watch?v=DNWLIAK4BUY)
- Thanks to LiveKit for providing real-time communication tools.
- Thanks to Groq for their powerful language models.
- Thanks to Deepgram and Cartesia for their speech-to-text and text-to-speech technologies.

