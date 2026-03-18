import requests
import time

# KROK 1: Twój token (Pamiętaj: nie udostępniaj go publicznie!)
TOKEN = "moj token do bota"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# KROK 2: Sprawdź, czy bot żyje
def sprawdz_bota():
    response = requests.get(f"{BASE_URL}/getMe")
    bot_info = response.json()
    if bot_info.get("ok"):
        bot = bot_info["result"]
        print(f"✅ Bot działa jako: {bot['first_name']} (@{bot['username']})")
    else:
        print("❌ Błąd! Sprawdź, czy token jest poprawny.")

# KROK 3: Funkcja Echo Bota (odwraca tekst)
def run_echo_bot(duration_seconds=60):
    offset = None
    end_time = time.time() + duration_seconds
    print(f"🦞 Bot będzie działał przez {duration_seconds} sekund. Wyślij coś z telefonu!")
    
    while time.time() < end_time:
        params = {"timeout": 5, "offset": offset}
        try:
            response = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=10)
            for update in response.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")
                
                if text and chat_id:
                    reversed_text = text[::-1]
                    requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": reversed_text})
                    print(f"📨 Odebrano: {text} -> Wysłano: {reversed_text}")
        except Exception as e:
            print(f"⚠️ Błąd: {e}")
            time.sleep(2)

# URUCHOMIENIE
if __name__ == "__main__":
    sprawdz_bota()
    run_echo_bot(60) # Bot działa przez minutę
