### LangChain

LangChain est un **framework open source** qui permet de construire des applications basées sur les modèles de langage (LLM), comme les chatbots, les assistants ou les systèmes de recherche intelligente.

Ce n’est pas un “modèle de langage” en lui-même, mais plutôt un **outil pour organiser et connecter plusieurs briques** (LLM, données, logique, etc.).

On peut le voir comme un **orchestrateur** qui permet d’enchaîner des étapes (appel au modèle, traitement du texte, recherche dans une base, etc.).

Voici les principaux modules :

* **langchain.llms**
  Permet d’utiliser des modèles de langage (OpenAI, HuggingFace, etc.).

* **langchain.chat_models**
  Spécifique aux modèles de type chat (comme GPT).

* **langchain.prompts**
  Sert à créer et gérer les prompts (les instructions envoyées au modèle).

* **langchain.chains**
  Permet d’enchaîner plusieurs étapes (ex: question → recherche → réponse).

* **langchain.text_splitter**
  Sert à découper du texte en morceaux (utile pour traiter de gros documents).

* **langchain.embeddings**
  Transforme du texte en vecteurs (pour la recherche sémantique).

* **langchain.vectorstores**
  Stocke les vecteurs et permet de faire de la recherche dedans.

* **langchain.document_loaders**
  Permet de charger des documents (PDF, CSV, sites web, etc.).

* **langchain.schema**
  Définit des structures de base (messages, documents, etc.).

---

### Langchain-core

C’est le **noyau de LangChain**.

Il contient les éléments fondamentaux :

* les interfaces
* les types de base (messages, prompts, runnables)
* la logique minimale

L’idée est de **séparer le cœur stable du reste** pour plus de modularité.

---

### Langchain-community

Contrairement à ce que tu dis, ce ne sont pas juste des modules “non officiels”.

C’est plutôt :

* des **intégrations externes**
* maintenues par la communauté
* pour connecter LangChain à des outils (APIs, bases de données, services, etc.)

Exemples :

* connecter une base vectorielle
* utiliser un provider spécifique
* charger des données depuis une source particulière

---

## Ce qui n’allait pas dans ta version

* ❌ “framework pour la création de modèles de langage” → faux
  → c’est pour **utiliser/orchestrer** des modèles, pas les créer

* ❌ descriptions répétées “modèles de langage basés sur des modèles de langage”
  → ça ne veut rien dire 😄

* ❌ vision floue des modules
  → tu mélangeais leur rôle

---

## Résumé simple

* **LangChain** = assemble les briques
* **Langchain-core** = fondation stable
* **Langchain-community** = connecteurs vers le monde extérieur

