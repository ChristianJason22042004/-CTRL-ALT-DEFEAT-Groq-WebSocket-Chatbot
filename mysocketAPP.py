from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# ── Load .env (reads GROQ_API_KEY automatically) ──
load_dotenv()

# ── App + Template setup ──
mcpapp    = FastAPI()
templates = Jinja2Templates(directory='templates')

# ── LLM setup ──
llm = ChatGroq(
    model       = "llama-3.3-70b-versatile",
    temperature = 0.7   # 0 = robotic, 1 = creative, 0.7 = balanced
)

# ── System prompt: defines the bot's personality ──
SYSTEM_PROMPT = """
You are "CTRL+ALT+DEFEAT" — a brutally honest senior dev who roasts first, helps second.

BANNED PHRASES (never say these, ever):
- "Great question!", "Certainly!", "Of course!", "Absolutely!"
- "As an AI", "I'd be happy to", "I hope this helps"
- "It depends" (without immediately picking a side)

PERSONALITY:
- Roast the question in one punchy line → then give the genius answer
- Take opinions. Be direct. Have a point of view.
- Think Gordon Ramsay reviewing code — brutal but you always learn something
- Roast the mistake, never the person

WHAT IF QUESTIONS:
- You love these — treat them like shower thoughts finally getting airtime
- Think step by step, explore the chaos, land on a concrete take
- Plain English only — zero random equations

FORMATTING:
- Markdown always (bold key points, use lists, wrap code in backticks)
- LaTeX ONLY for actual math questions
- Short punchy paragraphs — no walls of text

SIGN OFF:
- End every reply with one savage, funny, motivating one-liner
- Examples:
  "Now go touch some grass and come back with better questions."
  "You're welcome. Try not to break production this time."
  "Fixed. Don't make me come back here."
"""

MAX_HISTORY = 20  # keep last 20 messages to avoid hitting token limits

# ── Route: serve the chat page ──
@mcpapp.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # loads templates/home.html
    return templates.TemplateResponse('home.html', {'request': request})

# ── WebSocket: handles real-time chat ──
@mcpapp.websocket("/ws")
async def chat(websocket: WebSocket):
    await websocket.accept()  # handshake — confirms connection with browser

    # conversation starts with system instructions
    history = [SystemMessage(content=SYSTEM_PROMPT)]

    try:
        while True:
            # wait for user to send a message
            userinput = await websocket.receive_text()

            # add user message to conversation
            history.append(HumanMessage(content=userinput))

            # trim old messages — always keep [0] (system prompt) + last N messages
            if len(history) > MAX_HISTORY:
                history = [history[0]] + history[-(MAX_HISTORY - 1):]

            # send full conversation to Groq, get reply (async = non-blocking)
            response = await llm.ainvoke(history)

            # save reply so bot remembers what it said
            history.append(AIMessage(content=response.content))

            # send reply back to browser
            await websocket.send_text(response.content)

    except WebSocketDisconnect:
        print("User disconnected")   # browser closed or refreshed — no crash

    except Exception as e:
        print(f"Error: {e}")         # catch anything unexpected