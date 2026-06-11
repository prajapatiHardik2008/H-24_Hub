from pyrogram import Client
import asyncio
import os
import dotenv
import zipfile
from ui_handler import UIHandler

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
    UI.custom_print(f"Created zip file: {zip_path}")
    return zip_path

def progress(current, total):
        #UI.show_loading(f"Uploading... {current * 100 / total:.1f}%")
        UI.custom_print(f"{current * 100 / total:.1f}% uploaded")

app = Client("my_session", api_id = api_id , api_hash = api_hash)

async def main(file_path):
    async with app:
        UI.custom_print("Uploading file as zip format...")
        await app.send_document(chat_id="me",document =file_path, progress=progress)
        UI.custom_print("File uploaded successfully!")
        UI.custom_print("Cleaning up...")
        os.remove(file_path)
    
if __name__ == "__main__":
    file_path = input("Enter the path of the file to upload: ")
    if os.path.exists(file_path):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        file_path = make_zip(file_path)
        UI.custom_print(f"Uploading {file_path}...")
        loop.run_until_complete(main(file_path))
    else:
        UI.custom_print("Error: Invalid file path!", style="red")