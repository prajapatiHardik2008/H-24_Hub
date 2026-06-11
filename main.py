from saved_files import fetch_saved_files
from upload_file import main as upl ,make_zip, progress as progress_of_upload
from download_file import download_file
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

async def upload(file_path):
    file_path = make_zip(file_path)
    await upl(file_path=file_path)

async def create_repo(repo_name):
    Repos = []
    async with app:
        async for message in app.get_chat_history("me", limit=50):
            # Check karte hain ki message mein document (file) hai ya nahi
            if message.document:
                file_name = message.document.file_name
                file_id = message.id
                Repos.append(file_name)

            UI.custom_print("Checking is name Available ...","blue")
            current_name = repo_name
            while current_name in Repos:
                # User se naya naam maango (Terminal input)
                UI.custom_print(f"Error: {current_name} is already taken.", "red")
                current_name = input("Please enter a different repo name: ")
            
            UI.custom_print(f"Repo name '{current_name}' is available!", "green")
            return current_name   


async def down(repo_name):
    await download_file()

if __name__ == "__main__":
    UI.custom_print(r'''
                    

   ::   .:        .:::.     .::      ::   .:      ...    :::   :::::::.  
 ,;;   ;;,      ,;'``;.  ,;';;     ,;;   ;;,     ;;     ;;;    ;;;'';;' 
,[[[,,,[[[      ''  ,[[',[' [[    ,[[[,,,[[[    [['     [[[    [[[__[[\.
"$$$"""$$$ cccc .c$$P'  $P__$$c   "$$$"""$$$    $$      $$$    $$""""Y$$
 888   "88o    d88 _,oo,`"""88"    888   "88o   88    .d888   _88o,,od8P
 MMM    YMM    MMMUP*"^^    MM     MMM    YMM    "YmmMMMM""   ""YUMMMP" 
                                                                        
                                                                        
                                                                                                                                                                                             

''',"blue")
    
    while True:
        UI.custom_print("-----------------------------------","red")
        UI.custom_print("             H-24 's HUB           ","red")
        UI.custom_print("-----------------------------------","red")
        UI.custom_print("[+] 1 Create your repo ","green")
        UI.custom_print("[-] 2 Clone your repo ","yellow")
        UI.custom_print("[+] 3 View  your repo ","pink")
        UI.custom_print("[*] 4 Exit  ","red")
        UI.custom_print("-----------------------------------","red")

        choice = int(input("[+] Enter your choice ::- "))
        if choice == 4:
            break
        elif choice == 1:
            file_path = input("[+] Enter the path of the file to upload: ")
            if os.path.exists(file_path):
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                UI.custom_print(f"Uploading {file_path}...","green")
                loop.run_until_complete(upload(file_path))
            else:
                UI.custom_print("Error: Invalid file path!","red")
        elif choice == 2:
            user_file = input("Enter the File name to Download::- ")
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Run the coroutine in the manually created loop
            loop.run_until_complete(download_file(user_file))
        elif choice >4:
            UI.custom_print("[!]Please Enter a valid choice ","red")
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(fetch_saved_files())
