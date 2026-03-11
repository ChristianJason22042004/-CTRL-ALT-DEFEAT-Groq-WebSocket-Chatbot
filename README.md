# ⚡ CTRL+ALT+DEFEAT — Groq WebSocket Chatbot

> A senior dev AI assistant that helps first, always — direct, honest, and genuinely useful.  
> Built with **FastAPI**, **WebSockets**, **LangChain**, and **Groq's ultra-fast LLM inference**.

---

## 🖼️ Preview

```
● Connected

┌─────────────────────────────────────────┐
│              What is recursion?         │  ← you
│                                         │
│ Recursion is when a function calls      │  ← bot
│ itself until a base case stops it.      │
│                                         │
│ def countdown(n):                       │
│     if n == 0: return   # base case     │
│     print(n)                            │
│     countdown(n - 1)    # calls itself  │
│                                         │
│ Without the base case, it runs forever  │
│ and crashes with a stack overflow.      │
│                                         │
│ That's the concept locked in.           │
│ Build something with it.                │
└─────────────────────────────────────────┘
[ Ask anything...              ]  [ Send ]
```

---

## 🚀 Features

- **Real-time chat** via WebSockets — no page reloads, instant responses
- **Markdown rendering** — bold, lists, code blocks all render beautifully
- **LaTeX math support** — inline `$x^2$` and block `$$\int_0^\infty$$` formulas
- **Conversation memory** — bot remembers the last 20 messages
- **Smart history trimming** — never loses the system prompt, silently drops oldest messages
- **Live status indicator** — shows Connected / Thinking... / Disconnected in real time
- **XSS safe** — user input is never rendered as HTML

---

## 🗂️ Project Structure

```
project/
│
├── mysocketAPP.py       # FastAPI backend — WebSocket server + LLM logic
├── .env                 # Your secret API key (never commit this!)
├── requirements.txt     # Python dependencies
│
└── templates/
    └── home.html        # Frontend — chat UI with JS, CSS, Markdown + MathJax
```

---

## ⚙️ How It Works

```
Browser                          FastAPI + Groq
   │                                   │
   │──── WebSocket Handshake ────────→ │
   │←─── Connection Accepted ───────── │
   │                                   │
   │──── "What is recursion?" ───────→ │
   │         LangChain builds history  │
   │         Groq LLM generates reply  │
   │←─── "Oh look, recursion!..." ──── │
   │                                   │
   │  (tunnel stays open forever)      │
```

### Message Flow

1. User types a message → hits **Enter** or clicks **Send**
2. Message appears instantly as a blue bubble (optimistic UI)
3. Text is sent through the **WebSocket tunnel** to FastAPI
4. FastAPI appends it to `history` as a `HumanMessage`
5. Full conversation history is sent to **Groq API** via LangChain
6. Groq returns a reply → appended to history as `AIMessage`
7. Reply sent back through WebSocket to the browser
8. Browser renders it with **Markdown + MathJax** as a grey bubble

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) | Web server + WebSocket handler |
| LLM | [Groq](https://groq.com/) | Ultra-fast LLM inference |
| LLM Framework | [LangChain](https://www.langchain.com/) | Message history management |
| Model | `llama-3.3-70b-versatile` | The actual AI brain |
| Frontend | Vanilla HTML/CSS/JS | Chat UI |
| Markdown | [marked.js](https://marked.js.org/) | Renders bot's Markdown replies |
| Math | [MathJax 3](https://www.mathjax.org/) | Renders LaTeX formulas |
| Config | python-dotenv | Loads API key from `.env` |

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/ChristianJason22042004/-CTRL-ALT-DEFEAT-Groq-WebSocket-Chatbot.git
cd -CTRL-ALT-DEFEAT-Groq-WebSocket-Chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your `.env` file

```bash
# Create .env in the project root
touch .env
```

Add your Groq API key inside `.env`:

```
GROQ_API_KEY=gsk_your_key_here
```

> Get your free API key at [console.groq.com](https://console.groq.com)

### 5. Run the server

```bash
uvicorn mysocketAPP:mcpapp --reload
```

> `mysocketAPP` = your filename (`mysocketAPP.py`) — `mcpapp` = the FastAPI instance inside it (`mcpapp = FastAPI()`)

### 6. Open the app

```
http://localhost:8000
```

---

## 📋 Requirements

Create a `requirements.txt` with:

```
fastapi
uvicorn
langchain-core
langchain-groq
python-dotenv
jinja2
```

---

## 🧠 Bot Personality

The bot is configured via `SYSTEM_PROMPT` in `mysocketAPP.py`. It is designed to behave like a **senior software engineer and technical mentor** — direct, honest, and genuinely helpful.

**Identity:**
- 15+ years of experience, strong opinions backed by reasoning
- Treats beginners and seniors the same: with clarity and respect
- Dry wit is fine — but help always comes first, never at the user's expense

**Core rules the bot follows:**
- Answer first, explain second — lead with the solution, not the preamble
- Always back up points with working code examples
- Call out edge cases and gotchas even when not asked
- Give a concrete recommendation when asked — never sits on the fence
- Admits uncertainty honestly rather than guessing

**Banned phrases (zero tolerance):**
- "Great question!", "Certainly!", "Absolutely!", "Sure thing!"
- "As an AI", "I'd be happy to", "I hope this helps"
- "It depends" — unless immediately followed by exactly what it depends on

**Greeting behaviour:**
- Responds naturally and warmly — short, human, no sign-off
- Example: *"Hey! What are you working on?"*

**Sign-off behaviour:**
- A single closing line appears ONLY after substantive technical answers
- Never on greetings, small talk, yes/no answers, or follow-up questions
- Examples:
  > *"Now go ship it."*
  > *"That's the hard part done — the rest is just execution."*
  > *"One solid concept at a time — that's how good engineers are made."*

---

## 🔧 Configuration

| Variable | Location | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | `.env` | — | Your Groq API key (required) |
| `MAX_HISTORY` | `mysocketAPP.py` | `20` | Max messages kept in memory |
| `temperature` | `mysocketAPP.py` | `0.5` | LLM creativity (0=robotic, 1=wild) |
| `model` | `mysocketAPP.py` | `llama-3.3-70b-versatile` | Groq model to use |

### Tuning `temperature`

```
0.0 → "The capital of France is Paris."          (always identical, robotic)
0.5 → "Paris is the capital of France."          (focused, consistent ✅)
0.7 → "Paris! City of love and overpriced coffee." (more creative, less predictable)
1.0 → wildly creative, occasionally unhinged
```

> Set to `0.5` for production — more focused and reliable answers than `0.7`.

### Tuning `MAX_HISTORY`

```
Higher → bot remembers more context, but uses more tokens (slower/costlier)
Lower  → bot forgets older messages faster, but stays snappy
```

---

## 🔒 History Trimming

The bot keeps a **sliding window** of conversation history:

```python
MAX_HISTORY = 20

if len(history) > MAX_HISTORY:
    history = [history[0]] + history[-(MAX_HISTORY - 1):]
```

```
[SystemPrompt] [H1] [A1] [H2] [A2] ... [H10] [A10] [H11]
      ↑                                                ↑
  always kept                                    newest kept

After trim:
[SystemPrompt] [A1] [H2] [A2] ... [H10] [A10] [H11]
                ↑
           H1 dropped (oldest)
```

The **SystemPrompt is always preserved** at index `[0]` — the bot never forgets its personality.

---

## 🌐 WebSocket Events

| Event | Fires when | Action |
|---|---|---|
| `ws.onopen` | Connection established | Enable input, show green ● |
| `ws.onclose` | Connection dropped | Disable input, show red ● |
| `ws.onerror` | Connection error | Show red ● |
| `ws.onmessage` | Bot reply received | Render bubble, re-enable send |

---

## 🎨 UI Status Indicators

| Status | Color | Meaning |
|---|---|---|
| ● Connected | 🟢 Green | Ready to chat |
| ● Thinking... | 🟠 Orange | Waiting for bot reply |
| ● Disconnected | 🔴 Red | Server down or tab refreshed |

---

## 🔐 Security Notes

- **User input** uses `textContent` (not `innerHTML`) — prevents XSS attacks
- **Bot replies** use `innerHTML` via `marked.parse()` — safe since output is from your controlled LLM
- **API key** lives in `.env` — never hardcoded, never committed to git

Add `.env` to your `.gitignore`:

```
# .gitignore
.env
venv/
__pycache__/
```

---

## 📡 API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Serves the chat UI (`home.html`) |
| `WebSocket` | `/ws` | Real-time chat connection |

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and build on. Just give credit where it's due.

---

## 🙌 Acknowledgements

- [Groq](https://groq.com/) for blazing fast LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) for the cleanest Python web framework
- [LangChain](https://www.langchain.com/) for message history management
- [marked.js](https://marked.js.org/) for Markdown rendering
- [MathJax](https://www.mathjax.org/) for beautiful math typesetting

---

*Built with ☕ and a complete disregard for imposter syndrome.*
