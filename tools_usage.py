from langchain.tools import tool
from langchain_groq import ChatGroq
import os
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


llm = ChatGroq(model="openai/gpt-oss-120b",api_key=api_key,temperature=0)
store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    
    return store[session_id]

@tool
def search_moive_database(query)->str:
    """
    search the moive name in the text file and when you found it return the description or plot of the moive.
    
    :param query: Description
    """
    documents = []
    
    with open("movies.txt","r") as file:
        text_value = file.readlines()
    for lines in text_value:
        documents.append(lines.strip())
    
    vector_store = Chroma.from_texts(texts=documents,embedding=embeddings)
    results = vector_store.similarity_search(query,k=1)
    
    if results:
        return results[0].page_content
    else:
        return "Movie not playing."
            
@tool
def book_ticket(movie_name:str,persons:int)->str:
    """
    After succesfully finding the movie book the movie ticket with the name and number of persons.
        
    :param movie_name: Description
    :type movie_name: str
    :param persons: Description
    :type persons: int
    """
    with open("bookings.txt","a") as file:
        temp_str = "Booked "+str(persons)+" Tickets for the movie "+movie_name+"\n"
        file.writelines(temp_str)
        return "Success Ticket Confirmed."

@tool
def get_ticket_price(movie_name:str)->str:
    """
    get the price of a single ticket for a specific movie
    returns the price as string
    """  
    if "Bahubali" in movie_name:
        return "15"
    else: return "10"
    
tools = [search_moive_database,book_ticket,get_ticket_price]

prompt = ChatPromptTemplate.from_messages([
    ("system","you are a helpful cinema concierge. use the provided tools to search for a moive in the files and search if it exists tell the total cost of the ticket per person and total cost and book a ticket for that movie. If a moive is not found, do not book it and tell the user the movie is not playing."),
    ("placeholder", "{chat_history}"),
    ("human","{input}"),
    ("placeholder","{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm,tools,prompt)

agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
print("---Agent Starting----")

while True:
    user_input = input("User: ")
    
    if user_input.lower() in ["quit","exit","no"]:
        break
    
    response = agent_with_chat_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "session_1"}})
    print(f"Agent: {response['output']}")