#  langchain.agents : Création d'agents
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

load_dotenv()

#  langchain.tools : Création d'outils
from langchain.tools import tool

#  langchain.community.tools.tavaly_search : Outil de recherche sur Tavaly
# Tavily est un moteur de recherche conçu spécifiquement 
# pour les agents d'intelligence artificielle (IA) 
# et les applications de RAG (Retrieval-Augmented Generation). 
# Contrairement aux moteurs de recherche classiques pour humains, 
# il renvoie des données structurées et nettoyées, 
# optimisées pour être directement ingérées par 
# un grand modèle de langage (LLM)
from langchain_community.tools.tavily_search import TavilySearchResults

#  langchain_mistralai : Modèle de langage MistralAI
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
import os

#  langfuse.langchain : CallbackHandler pour langfuse
# from langfuse.langchain import CallBackHander

#  datetime : Module pour la gestion des dates et heures
from datetime import datetime

#  dotenv : Module pour la gestion des variables d'environnement
# (déjà importé en haut du fichier)


@tool
def research_tool(query: str) -> str:
    # juste pour dire que cette fonction peut etre appeler par un agant ai comme outils externe
    """
    Make a research on the web for the query
    """
    tavaly = TavilySearchResults(max_results=3)
    return str(tavaly.invoke(query))

@tool
def vital_charge() -> str:
    """
    Return the users's monthly vital charges(rent, food, bills, etc,)
    """
    charges = {
        "rent": "$500",
        "food": "$200",
        "children_schooling": "$100",
        "electricity": "$100",
        "internet": "$40",
        "transport": "$100"
    }
    return str(charges)

@tool
def salary() -> str:
    """
    return the users's monthly salary
    """
    return "$1000"


@tool
def get_current_date() -> str:
    """
    Return the current date
    """
    return str(datetime.now())

system_prompt = """
    Role: You are a helpful assistant with acces to tools.

    goal: Your main goal is to analyse something the user wants to buy check if it is within their budget after vital charges, and provide financial advice.
    Consider that the user receives their salary between the 1st and 5th of each month.
    If the purchase is not affordable right now, suggest eht best time to buy it and how to save for it.

    you can:
    - Search the web for current information
    - Perfoem calculations
    - Get the current time

    think step-by-step and use tools when needed to provide accurate answers.
    Be concise but thorough.
"""

# create agent
# agent = create_react_agent(
#     model=ChatMistralAI(model="mistral-large-latest", temperature=0.0),
#     tools=[research_tool, vital_charge, salary, get_current_date],
#     prompt=system_prompt,
# )

model = ChatOpenAI(
    model="mistralai/mistral-large",
    api_key=os.getenv("OPEN_ROUTER"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.0,
)

agent = create_react_agent(
    model=model,
    tools=[research_tool, vital_charge, salary, get_current_date],
    prompt=system_prompt,
)