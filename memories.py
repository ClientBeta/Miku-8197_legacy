import json
from datetime import datetime

def load_mem(file_path="braincells.json"):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            # Convert ISO strings to datetime
            for user_data in data.values():
                if "lastactive" in user_data and isinstance(user_data["lastactive"], str):
                    user_data["lastactive"] = datetime.fromisoformat(user_data["lastactive"])
            return data
    except Exception as e:
        print(f"[!] Failed to load memory: {e}")
        return {}
def save_mem(data, file_path="braincells.json"):
    try:
        # Convert datetime to ISO string
        save_data = {}
        for userid, user_data in data.items():
            save_data[userid] = {
                "history": user_data.get("history", []),
                "lastactive": user_data["lastactive"].isoformat() if isinstance(user_data.get("last_active"), datetime) else datetime.now().isoformat()
            }
        with open(file_path, "w") as f:
            json.dump(save_data, f, indent=2)
    except Exception as e:
        print(f"[!] Failed to save memory: {e}")