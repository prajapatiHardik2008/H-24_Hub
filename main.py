from saved_files import fetch_saved_files,search_repo
from upload_file import main as upl ,make_zip
from download_file import download_file
from pyrogram import Client
import asyncio
import os
import dotenv
from ui_handler import UIHandler,alert_warning
import shutil
import stat
import time 
import random
from cryptography.fernet import Fernet





security_points = [
    "The system-generated key is strictly random.",
    "Once the file is uploaded, access without the key is impossible.",
    "Never share your secret key with anyone.",
    "Use only the H-24 Decryptor to decrypt your files.",
    "Use this method for particular file not for folder "
]



UI = UIHandler()

dotenv.load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
#my favourite spinner types 
sp = ["aesthetic","clock","hearts","runner","smiley","earth"]

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
                #file_id = message.id
                Repos.append(file_name)

            UI.show_loading("Checking is name Available ...","blue",random.choice(sp))
            current_name = repo_name
            while current_name in Repos:
                # User se naya naam maango (Terminal input)
                UI.custom_print(f"Error: {current_name} is already taken.", "red")
                current_name = input("Please enter a different repo name: ")
            print(Repos)
            UI.custom_print(f"Repo name '{current_name}' is available!", "green")
            return current_name   

def remove_readonly(func, path, ):
    # Agar file read-only hai, toh permission change karke delete karo
    os.chmod(path, stat.S_IWRITE)
    func(path)
# async def down(repo_name):
#     await download_file()


class  privet_upload():
    def __init__(self):
        alert_warning("H-24 SECURITY PROTOCOL", security_points)
        self.key = Fernet.generate_key()
        UI.custom_print(f"Your Key :- {self.key}","red")

    async def upload(self,file_path):
        file_path = make_zip(file_path)
        await upl(file_path=file_path)

  
    def encryptFile_upload(self,file_path):
        f =  Fernet(self.key)
        with open(file_path,"rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)

        with open(file_path+".locked","wb")  as file:
            file.write(encrypted_data)
        locked_path = file_path+".locked" 
        UI.custom_print("[!] Your file Encrypted successfully ! ","green")
        return locked_path

    def decrypt(self,file_path):
        key_input = input("[+] Enter your key ::- ")
        try:
            f  = Fernet(key=key_input.encode())
            self.file_path = file_path
            with open(self.file_path,"rb") as file:
                file_data = file.read()

            decrypt_data = f.decrypt(file_data)
            self.file_path = self.file_path.replace(".locked","")
            with open(self.file_path,"wb") as file:
                file.write(decrypt_data)
            UI.custom_print("File Decrypted successfully !","green")
        except Exception as e:
            UI.custom_print(f"Decryption failed! Invalid Key. Error: {e}", "red")



pv_upload = privet_upload()

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
        UI.custom_print("[+] 3 View  your repo ","magenta")
        UI.custom_print("[+] 4 Search  your repo ","orange1")
        UI.custom_print("[+] 5 Upload  Privet File ","blue")
        UI.custom_print("[+] 6 Decrypt Privet file  ","orange1")
        UI.custom_print("[*] 7 Exit  ","red")
        UI.custom_print("-----------------------------------","red")
# 
        try:
            choice = int(input("[+] Enter your choice ::- "))
            if choice == 7:
                break
            elif choice == 1:
                file_path = input("[+] Enter the path of the file to upload: ")

                repo_name = input("[+] Enter the Repo name ::- ")
                if not repo_name.endswith(".zip"):
                    repo_name= f"{repo_name}.zip"

                loop = asyncio.get_event_loop()
                repo_name = loop.run_until_complete(create_repo(repo_name))
                if repo_name.endswith(".zip"):
                    repo_name = os.path.splitext(repo_name)[0]  
                UI.custom_print(f"[+] your repo name ::- {repo_name}","red")
                destination_dir = r"./upload/"+repo_name
                shutil.copytree(file_path, destination_dir)
                file_path = r"./upload/"+repo_name
                if os.path.exists(file_path):
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    UI.show_loading(f"Uploading {file_path}...","green",random.choice(sp))
                    loop.run_until_complete(upload(file_path))
                    if os.path.isdir(file_path):
                        try:
                            time.sleep(1)
                            shutil.rmtree(file_path,onerror=remove_readonly) 
                            UI.custom_print(f"Successfully cleaned up: {file_path}", "green")
                        except Exception as e:
                            UI.custom_print(f"Error :- {e}","red")
                    else:
                        os.remove(file_path)
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
            elif choice == 3:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(fetch_saved_files())
            elif choice == 4:
                src = input("[+] Enter your File to search ::- ")
                loop = asyncio.get_event_loop()
                loop.run_until_complete(search_repo(src))
            elif choice == 5:
                file_path = input("[+] Enter the file path: ")
                # os.path.exists use karna zyada safe hai
                if os.path.exists(file_path) and not os.path.isdir(file_path):
                    file_path = pv_upload.encryptFile_upload(file_path) # Yahan await ki zaroorat nahi
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    UI.show_loading(f"Uploading {file_path}...","green",random.choice(sp))
                    loop.run_until_complete(upload(file_path))
                else:
                    # alert_warning mein sirf message chahiye ya points?
                    # Tumne pehle list pass ki thi, ab ek specific warning message pass karo
                    alert_warning("SECURITY ERROR", ["This is a file-only operation.", "Folders are not supported."])
            elif choice ==  6:
                file_path = input("[+]Enter the file path")
                pv_upload.decrypt(file_path)
            else:
                UI.custom_print("[!]Please Enter a valid choice ","red")
        except ValueError as v:
            UI.custom_print(f"[!] Value error please enter a valid value {v}","red")
