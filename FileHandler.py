import logging
import os
from typing import List
logging.basicConfig(filename="notes.log",
                    level=logging.INFO,format="%(asctime)s -- %(levelname)s -- %(message)s"
                    )

class FileHandler:
    def __init__(self,Base_directory="./notes") -> None:
        self.BASE_DIR=Base_directory

    def open_file(self,path:str)->int:
        try:
            os.startfile(path)
            logging.info(f"File opened: {os.path.abspath(path)}")
            return 1
        except Exception as e:
            logging.error(f"File Failed to open at {os.path.abspath(path)} | Error: {e}")
            return -1

    def list_languages(self)->List[str]:
        languages=os.listdir(self.BASE_DIR)
        return languages
    
    def list_topics(self,lang:str)->List[str]:
        folder_path=os.path.join(self.BASE_DIR,lang)
        if not os.path.exists(folder_path):
            msg=f"Folder not found:{os.path.abspath(folder_path)}"
            logging.warning(msg)
            return ["folder doesn't exist"]
        else:
            return os.listdir(folder_path)
    
    def file_path(self,l:str,topic:str)->str:
        pre=os.path.join(self.BASE_DIR,l,topic)
        return pre