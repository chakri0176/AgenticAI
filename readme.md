# 🎬 The Cinema Concierge: An Autonomous Agentic AI

## 🚀 Overview

The Cinema Concierge is a stateful, autonomous AI agent designed to simulate a real-world customer service experience. Unlike traditional chatbots that simply retrieve information, this Agentic AI system reasons through problems, manages its own memory, and executes real-world actions (file I/O) to fulfill user requests.

It demonstrates the **ReAct (Reasoning + Acting)** pattern, where the AI:

1. **Thinks**: Analyzes the user's intent (e.g., "I want a movie about hacking").
2. **Searches**: Uses Semantic Search (RAG) to find relevant data even without keyword matches.
3. **Acts**: Autonomously calculates prices and "books" tickets by writing to the file system.

## 🧠 Why "Agentic AI"?

This project serves as a sample use case for **Agentic Workflows**, moving beyond simple Q&A bots.

| Feature | Standard Chatbot | Cinema Concierge Agent |
|---------|------------------|------------------------|
| **Logic** | Fixed "If/Else" or simple text generation | Dynamic Reasoning (Decides which tools to use) |
| **Data Source** | Training data only | RAG (Retrieves live data from Vector DB) |
| **Action** | Cannot touch external systems | Tool Calling (Executes Python functions) |
| **Memory** | Often stateless | Stateful (Remembers names & context via Session ID) |

## 🏗️ Architecture

The system follows a multi-step reasoning loop:

1. **Router** (Llama 3 via Groq): The brain that parses user input and selects tools.
2. **Memory** (RunnableWithMessageHistory): Stores conversation context (Session State).
3. **Retrieval Tool** (ChromaDB): Converts queries like "sinking boat" into vector embeddings to find semantically similar movies (e.g., "Titanic").
4. **Action Tool** (Python): Executes the booking logic and updates the local `bookings.txt` record.

## 🛠️ Tech Stack

- **LLM**: Llama 3-70b (via Groq API for ultra-fast inference)
- **Orchestration**: LangChain
- **Vector Store**: ChromaDB (Local persistent storage)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Language**: Python 3.10+

## 📂 Project Structure
```
AgenticAI/
├── movies.txt           # The knowledge base (RAG source)
├── agent.py             # Main application logic
├── bookings.txt         # Log file where the agent writes "actions"
├── requirements.txt     # Dependencies
├── .env                 # API Keys (Not uploaded to GitHub)
└── README.md            # Documentation
```

## ⚡ Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/chakri0176/AgenticAI.git
cd AgenticAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token
```

### 4. Run the Agent
```bash
python agent.py
```

## 💬 Example Workflow

**User**: "I want to watch a movie about hacking and simulation."

**Agent (Thought Process)**: *User is asking for a concept. I should use the search_movie_database tool with the query "hacking simulation".*

**Agent (Action)**: *Calls Vector DB. Finds "The Matrix".*

**Agent**: "I found 'The Matrix'. It is about a hacker discovering reality is a simulation. Would you like to book tickets?"

**User**: "Yes, book 2 tickets."

**Agent (Thought Process)**: *User wants to book. I need the price first. I will call get_ticket_price. Then I will calculate the total. Then I will call book_ticket.*

**Agent (Action)**: *Writes to bookings.txt.*

**Agent**: "Success! I have booked 2 tickets for The Matrix. Total cost is $20."

## 🔮 Future Improvements

- **Frontend**: Connect this backend to a Streamlit UI for a chat interface.
- **Database**: Migrate `bookings.txt` to an SQL database (SQLite/PostgreSQL).
- **Multi-Agent**: Separate the "Searcher" and "Booker" into two distinct agents using LangGraph.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue on [GitHub](https://github.com/chakri0176/AgenticAI/issues).

---

⭐ If you find this project helpful, please consider giving it a star!