# DevOps AI Chatbot 🤖

Un chatbot intelligent specialise en DevOps, propulse par Claude (Anthropic).
Projet realise dans le cadre d'un PFE sur l'IA agentique et le DevOps.

## Ce que fait ce projet

- Repond a toutes tes questions DevOps (Docker, Kubernetes, CI/CD...)
- **Garde la memoire** de la conversation (contexte conserve)
- Commandes speciales : `/clear`, `/history`, `/help`, `/exit`
- Base parfaite pour ajouter RAG, agents, et plus encore

## Architecture du projet

```
devops-ai-chatbot/
│
├── chatbot.py          # Le chatbot principal (tout le code)
├── requirements.txt    # Les dependances Python
├── .env.example        # Template pour ta cle API (sans la vraie cle)
├── .gitignore          # Fichiers a ne pas pusher sur GitHub
└── README.md           # Ce fichier
```

## Comment lancer le projet

### Etape 1 — Clone le repo
```bash
git clone https://github.com/TON_USERNAME/devops-ai-chatbot.git
cd devops-ai-chatbot
```

### Etape 2 — Installe les dependances
```bash
pip install -r requirements.txt
```

### Etape 3 — Configure ta cle API
```bash
# Copie le template
cp .env.example .env

# Ouvre .env et remplace "mets-ta-cle-ici" par ta vraie cle
# Obtiens ta cle sur : https://console.anthropic.com
```

### Etape 4 — Lance le chatbot
```bash
python chatbot.py
```

## Exemple de conversation

```
Toi: Mon pod Kubernetes est en CrashLoopBackOff, comment je debug ?

Bot: Voici les etapes pour diagnostiquer un CrashLoopBackOff :

1. Voir les logs du pod :
   kubectl logs <nom-du-pod> --previous

2. Decrire le pod pour voir les events :
   kubectl describe pod <nom-du-pod>

3. Causes les plus frequentes :
   - Variable d'environnement manquante
   - Image Docker introuvable
   - Manque de ressources (CPU/RAM)
   ...

Toi: /history
[Historique: 2 messages]

Toi: /clear
[Memoire effacee - Nouvelle conversation]
```

## Comprendre le code — Les concepts cles

### 1. L'appel API (comment parler a Claude)
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=SYSTEM_PROMPT,      # Personnalite du bot
    messages=conversation_history  # La memoire !
)
```

### 2. La memoire (comment le bot se souvient)
```python
# La memoire = juste une liste Python !
conversation_history = []

# Chaque message ajoute a la liste
conversation_history.append({"role": "user", "content": "..."})
conversation_history.append({"role": "assistant", "content": "..."})

# On envoie TOUTE la liste a chaque appel API
# Claude voit toute la conversation = il "se souvient"
```

### 3. Le system prompt (la personnalite du bot)
```python
SYSTEM_PROMPT = """Tu es un expert DevOps..."""
# Change ce texte pour changer le comportement du bot !
```

## Prochaines etapes (Phase 2 & 3)

- [ ] **Phase 2 - RAG** : Ajouter une base de connaissances avec tes docs DevOps
- [ ] **Phase 2 - ChromaDB** : Stocker les logs Kubernetes pour Q&A
- [ ] **Phase 3 - Agent** : Analyser les erreurs CI/CD automatiquement
- [ ] **Phase 3 - MCP** : Connecter le bot a GitHub, Slack, Prometheus

## Technologies utilisees

| Tech | Role |
|------|------|
| Python 3.11+ | Langage principal |
| Anthropic SDK | Connexion a Claude (LLM) |
| python-dotenv | Gestion securisee des cles API |

## Auteur

Projet PFE — Agentic AI + DevOps
