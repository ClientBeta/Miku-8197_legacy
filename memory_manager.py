# FAAAAAAAILED ATTEMPT AT A MEMORY MANAGER
# -ASSISTANT
import json
from datetime import datetime, timezone

def save_sessions(sessions, file_path="storage.json"):
# Something here
    serializable_data = {}
    for user_id, session_data in sessions.items():
        chat_session = session_data.get("chat")
        if not chat_session:
            continue

        serializable_history = [
            {"role": msg.role, "parts": [part.text for part in msg.parts]}
            for msg in chat_session.history
        ]
        
        serializable_data[user_id] = {
            "history": serializable_history,
            "last_active": session_data["last_active"].isoformat()
        }
        
    try:
        with open(file_path, "w", encoding="utf8") as f:
            json.dump(serializable_data, f, indent=4)
    except Exception as e:
        print(f"[memory_manager] Failed to save sessions: {e}")

def load_sessions(model, file_path="storage.json"):
    """
    Loads and reconstructs user chat sessions from a JSON file.
    It uses the saved history to initialize new chat session objects.
    """
    try:
        with open(file_path, "r", encoding="utf8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    reconstructed_sessions = {}
    for user_id, user_data in data.items():
        try:
            chat_session = model.start_chat(history=user_data["history"])
            
            last_active_dt = datetime.fromisoformat(user_data["last_active"])
            
            reconstructed_sessions[user_id] = {
                "chat": chat_session,
                "last_active": last_active_dt
            }
        except Exception as e:
            print(f"[memory_manager] Could not reconstruct session for user {user_id}: {e}")
            
    print(f"[memory_manager] Loaded and reconstructed {len(reconstructed_sessions)} user sessions.")
    return reconstructed_sessions
