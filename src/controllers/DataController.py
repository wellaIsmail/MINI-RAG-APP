from .BaseController import BaseController
from .ProjectControllers import ProjectControllers
from fastapi import UploadFile
from models import ResponseSignals
import re
import os 

class DataConroller(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scal = 1048576 #convert MB to Bytes
    

    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignals.FILE_TYPE_NOT_SUPPORTED
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scal:
            return False, ResponseSignals.FILE_SIZE_EXCEED
        return True, ResponseSignals.FILE_UPLOAD_SUCCESS
    def generate_unique_file_name(self,orig_file_name:str,projet_id:str):
        random_key = self.generate_random_string() 
        project_path = ProjectControllers().get_project_path(project_id=projet_id)
        clean_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
        )
        new_file_path = os.path.join(
            project_path,
            random_key + "_" + clean_file_name
        )
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string() 
        
            new_file_path = os.path.join(
                    project_path,
                    random_key + "_" + clean_file_name
            )
        return new_file_path

    def get_clean_file_name(self,orig_file_name:str):
        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name


