from pyrogram import Client
import asyncio
import os
import dotenv
from ui_handler import UIHandler
UI = UIHandler()
dotenv.load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

app = Client("my_session", api_id = api_id , api_hash = api_hash)

async def download_file(file_name):
    found = False
    async with app:
        # messages = await app.get_chat_history("me",limit=150)
        async for message in app.search_messages("me", query=file_name, limit=1):
            if message.document:
                found = True
                UI.custom_print(f"Downloading {file_name}...","yellow")
                download_dir = os.path.join(os.getcwd(), "Downloads") 
                
                #:
                download_folder = os.path.join(os.getcwd(), "Downloads")
                if not os.path.exists(download_folder):
                    os.makedirs(download_folder)

                # old path (folder + file name)
                final_path = os.path.join(download_folder, file_name)

                # Download 
                path = await app.download_media(message, file_name=final_path , progress= lambda c, t: UI.custom_print(f"Downloading {c*100/t} % ","pink") )
                UI.custom_print(F"File Downloaded !","green")
        if not found:
            UI.custom_print(f"File Not Found {file_name}","red")
if __name__ == "__main__":
    # Naya loop force karo
    user_file = input("Enter the File name to Download::- ")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)    
    
    # Run the coroutine in the manually created loop
    loop.run_until_complete(download_file(user_file))