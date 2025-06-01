
from enum import Enum

class ResponseSignals(Enum):
    FILE_VALIDATE_SUCCESS="File_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED="file_type_not_supported"
    FILE_UPLOAD_SUCCESS="File_uploaded_successfully"
    FILE_SIZE_EXCEED="file_size_exceeded"
    FILE_UPLOAD_FAILED="File_upload_Failed"
