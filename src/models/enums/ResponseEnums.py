
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
    PROJECT_NOT_FOUND="project_not_found"
    INSERT_INTO_VECTODB_ERROR="insert_into_vectordb_error"
    INSERT_INTO_VECTODB_SUCCESS="insert_into_vectordb_success"
    VECTOR_COLLECTION_RETRIVED="vectordb_collection_retrived"
    VECTORDB_SEARCH_ERROR= "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS="vectordb_search_success"
    RAG_ANSWER_ERROR="rag_answer_error"
    RAG_ANSWER_SUCCESS="rag_answer_success"
