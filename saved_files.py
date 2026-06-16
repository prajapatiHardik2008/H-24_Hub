from pyrogram import Client
import asyncio
import os
import dotenv
from ui_handler import UIHandler
import random
UI = UIHandler()
dotenv.load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

#my favourite spinner types 
sp = ["aesthetic","clock","hearts","runner","smiley","earth"]
app = Client("my_session",api_id=api_id,api_hash=api_hash)
async def fetch_saved_files():
    async with app:
        UI.show_loading("Fetching your saved messages...","gold1",random.choice(sp))
        # 'me' matlab Saved Messages
        async for message in app.get_chat_history("me", limit=50):
            # Check karte hain ki message mein document (file) hai ya nahi
            if message.document:
                file_name = message.document.file_name
                file_id = message.id
                UI.custom_print(f"ID: {file_id} | File: {file_name}","gray")
            
            # Agar sirf text hai
            elif message.text:
                text = message.text[:30] # Sirf shuru ke 30 characters
                UI.custom_print(f"ID: {message.id} | Text: {text}...","black")
async def search_repo(file_name_ser):
    # Extension handling
    if not file_name_ser.endswith(".zip"):
        file_name_ser += ".zip"
        
    found = False
    UI.show_loading("Searching your File ::- ", "gold1", random.choice(sp))
    
    async with app:
        async for message in app.get_chat_history("me", limit=50):
            if message.document and message.document.file_name == file_name_ser:
                UI.custom_print(f"[+] Your file Found as Name ::- {file_name_ser}", "green")
                found = True
                break  # File mil gayi, loop tod do
    
    if not found:
        # cleanup string for display
        clean_name = file_name_ser.replace(".zip", "")
        UI.custom_print(f"[!] File {clean_name} Not found ", "red")
        
    return found # True/False return karna better practice hai
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_saved_files())