from pyrogram import Client
import asyncio
import os
import dotenv
import zipfile
from ui_handler import UIHandler
import stat
import shutil
import time
dotenv.load_dotenv()

UI = UIHandler()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
def make_zip(source_path):
    
    zip_path = source_path + ".zip"
    
    
    if os.path.isdir(source_path):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Zip ke andar ka structure maintain karne ke liye
                    arcname = os.path.relpath(file_path, os.path.dirname(source_path))
                    zipf.write(file_path, arcname)
    
    else:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(source_path, os.path.basename(source_path))
    UI.custom_print(f"Created zip file: {zip_path}","green")
    return zip_path

def progress(current, total):
        #UI.show_loading(f"Uploading... {current * 100 / total:.1f}%")
        UI.custom_print(f"{current * 100 / total:.1f}% uploaded","green")

app = Client("my_session", api_id = api_id , api_hash = api_hash)
def remove_readonly(func, path, excinfo):
    # Agar file read-only hai, toh permission change karke delete karo
    os.chmod(path, stat.S_IWRITE)
    func(path)

async def main(file_path):
    async with app:
        UI.custom_print("Uploading file as zip format...","green")
        await app.send_document(chat_id="me",document =file_path, progress=progress)
        UI.custom_print("File uploaded successfully!","green")
        UI.custom_print("Cleaning up...","red")
        
        if os.path.isdir(file_path):
            try:
                time.sleep(1) 
                shutil.rmtree(file_path, onerror=remove_readonly)
                UI.custom_print(f"Successfully cleaned up: {file_path}", "green")
            except Exception as e:
                UI.custom_print(f"Error cleaning up: {e}", "red")
        else:
            try:
                if os.path.exists(file_path):
                    os.chmod(file_path,stat.S_IWRITE)
                    os.remove(file_path)
            except Exception as e:
                UI.custom_print(f"Error removing file: {e}", "red")

            
if __name__ == "__main__":
    file_path = input("Enter the path of the file to upload: ")
    if os.path.exists(file_path):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        file_path = make_zip(file_path)
        UI.custom_print(f"Uploading {file_path}...","green")
        loop.run_until_complete(main(file_path))
    else:
        UI.custom_print("Error: Invalid file path!", style="red")