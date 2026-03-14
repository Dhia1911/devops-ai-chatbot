"""
DevOps AI Chatbot - Projet Fin d'Etudes
Un chatbot avec memoire specialise en DevOps
Utilise l'API Groq (LLaMA)
"""

import os
from dotenv import load_dotenv
import groq
from groq import Groq

# Charge les variables d'environnement depuis .env
load_dotenv()

# ============================================================
# CONFIGURATION DU CHATBOT
# ============================================================
SYSTEM_PROMPT = """Tu es un expert DevOps assistant. Tu aides avec :
- Docker, Kubernetes, CI/CD
- GitHub Actions, Jenkins, GitLab CI
- Monitoring, logs, alertes
- Infrastructure as Code (Terraform, Ansible)
- Debugging et troubleshooting

Reponds toujours en francais. Sois concis et pratique.
Quand tu donnes des commandes, utilise des blocs de code.
"""

# ============================================================
# INITIALISATION DU CLIENT GROQ
# ============================================================
def create_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERREUR: GROQ_API_KEY manquante dans le fichier .env")
        print("Cree un fichier .env avec: GROQ_API_KEY=ta-cle-ici")
        exit(1)
    return Groq(api_key=api_key)


# ============================================================
# FONCTION PRINCIPALE : ENVOYER UN MESSAGE
# ============================================================
def chat(client, conversation_history, user_message):
    """
    Envoie un message et retourne la reponse.
    conversation_history = la memoire du chatbot (liste de messages)
    """
    # Ajoute le message de l'utilisateur a l'historique
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Appel a l'API Groq avec tout l'historique (= la memoire)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=messages
    )

    # Extrait le texte de la reponse
    assistant_message = response.choices[0].message.content

    # Ajoute la reponse a l'historique pour la prochaine fois
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message, conversation_history


# ============================================================
# COMMANDES SPECIALES DU CHATBOT
# ============================================================
def handle_special_commands(user_input, conversation_history):
    """
    Gere les commandes comme /clear, /history, /exit
    Retourne True si c'est une commande speciale
    """
    if user_input == "/exit":
        print("\nAu revoir ! Bon courage pour ton PFE 🚀")
        exit(0)

    elif user_input == "/clear":
        conversation_history.clear()
        print("\n[Memoire effacee - Nouvelle conversation]\n")
        return True

    elif user_input == "/history":
        if not conversation_history:
            print("\n[Pas encore de conversation]\n")
        else:
            print(f"\n[Historique: {len(conversation_history)} messages]\n")
            for i, msg in enumerate(conversation_history):
                role = "Toi" if msg["role"] == "user" else "Bot"
                # Affiche les 80 premiers caracteres
                preview = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
                print(f"  {i+1}. {role}: {preview}")
            print()
        return True

    elif user_input == "/help":
        print("""
Commandes disponibles:
  /clear    → Effacer la memoire du chatbot
  /history  → Voir l'historique de la conversation
  /help     → Afficher cette aide
  /exit     → Quitter le chatbot
        """)
        return True

    return False  # Pas une commande speciale


# ============================================================
# BOUCLE PRINCIPALE DU CHATBOT
# ============================================================
def main():
    print("=" * 55)
    print("  DevOps AI Chatbot - Propulse par Groq (LLaMA)")
    print("=" * 55)
    print("Pose tes questions DevOps en francais !")
    print("Tape /help pour voir les commandes disponibles")
    print("-" * 55)

    # Cree le client API
    client = create_client()

    # La memoire du chatbot - liste vide au depart
    conversation_history = []

    # Boucle infinie - le chatbot tourne jusqu'a /exit
    while True:
        try:
            # Recupere l'input de l'utilisateur
            user_input = input("\nToi: ").strip()

            # Ignore les messages vides
            if not user_input:
                continue

            # Verifie si c'est une commande speciale (/clear, /exit...)
            if user_input.startswith("/"):
                handle_special_commands(user_input, conversation_history)
                continue

            # Envoie le message et recupere la reponse
            print("\nBot: ", end="", flush=True)
            response, conversation_history = chat(client, conversation_history, user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\nInterruption detectee. Au revoir !")
            break
        except groq.APIError as e:
            print(f"\nErreur API: {e}")
            print("Verifie ta cle API dans le fichier .env")


if __name__ == "__main__":
    main()
