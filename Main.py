import time
import requests

BOT_TOKEN = "8347163119:AAEs5xfqwUWBrL8qBCWtiEwNZcPyAUANbl0"

CHANNELS = [
    "@SS_Trader_17",
    "@Channel_One_test",
    "@Channel_two_test",
    "@Channel_three_test"
]

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

requests.get(f"{BASE_URL}/deleteWebhook?drop_pending_updates=True")

def get_updates(offset=None):
    try:
        url = f"{BASE_URL}/getUpdates?timeout=20"
        if offset:
            url += f"&offset={offset}"
        res = requests.get(url, timeout=25)
        return res.json()
    except Exception:
        return None

def copy_message(chat_id, from_chat_id, message_id):
    url = f"{BASE_URL}/copyMessage"
    data = {
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_id": message_id
    }
    try:
        requests.post(url, data=data)
    except Exception:
        pass

def main():
    print("Cloud bot is running 24/7...")
    last_update_id = None
    
    while True:
        updates = get_updates(last_update_id)
        if updates and updates.get("ok"):
            for result in updates.get("result", []):
                last_update_id = result["update_id"] + 1
                
                msg = result.get("message")
                if msg:
                    chat_id = msg.get("chat", {}).get("id")
                    msg_id = msg.get("message_id")
                    
                    for target in CHANNELS:
                        copy_message(target, chat_id, msg_id)
                        
        time.sleep(1)

if __name__ == "__main__":
    main()
