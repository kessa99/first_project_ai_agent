# Tools

## Tavaly

Tavily est un moteur de recherche conçu spécifiquement 
pour les agents d'intelligence artificielle (IA) 
et les applications de RAG (Retrieval-Augmented Generation).

le tool reasearch_tool(query: str) -> str, est un tools qui prends en paramtre 1 elements et qui doit retourner un string

tavaly = TavalySeardyResults(max_results=3) est un objet qui sert a faire une recherche web. et max_results est le nombre de resultat que tu veux avoir. Ici 3 donc cela veu dire que tu le limite a 3 elements

[
  {"title": "...", "url": "...", "content": "..."}
]

