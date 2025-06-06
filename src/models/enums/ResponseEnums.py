
from enum import Enum

class ResponseSignals(Enum):
    FILE_VALIDATE_SUCCESS="File_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED="file_type_not_supported"
    FILE_UPLOAD_SUCCESS="File_uploaded_successfully"
    FILE_SIZE_EXCEED="file_size_exceeded"
    FILE_UPLOAD_FAILED="File_upload_Failed"
    PROCESSING_FAILED="Processing_failed"
    PROCESSING_SCUCCESS="Processing_success"
    NO_FILES_ERROR="not_found_files"
    FILE_ID_ERROR="no_file_found_with_this_id"
