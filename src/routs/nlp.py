from fastapi import FastAPI,APIRouter, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import NLPController
import os
import aiofiles
from models import ResponseSignals
import logging
from .schemes.nlp import PushRequest, SearchRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk,Asset
from models.AssetModel import AssetModel
from models.enums.AssetTypeEnum import AssetTypeEnum

logger = logging.getLogger('uvicorn.error')

nlp_router=APIRouter(
    prefix= "/api/v1/nlp",
    tags=["api_v1","nlp"],
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(request:Request, project_id:str, push_request:PushRequest):
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
        )
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id= project_id)
    if not project:
        JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal": ResponseSignals.PROJECT_NOT_FOUND.value
            }
        )
    
    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
        )
    
    has_record = True
    page_no = 1
    inserted_items_count = 0
    idx = 0
    while has_record :
        page_chunks = await chunk_model.get_project_chunks(project_id=project.id, page_no=page_no)
        if len(page_chunks):
            page_no +=1
            
        if not page_chunks or len(page_chunks)==0:
            has_record = False
            
            break
        chunk_ids =  list(range(idx, idx + len(page_chunks)))
       
        idx += len(page_chunks)
        
        is_inserted = nlp_controller.index_into_vector_db(
            project=project,
            chunks= page_chunks,
            do_reset=push_request.do_reset,
            chunk_ids = chunk_ids
            )
        
        if not is_inserted :
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content= {
                    "signal":ResponseSignals.INSERT_INTO_VECTODB_ERROR.value
                }
            )
        inserted_items_count += len(page_chunks)
    return JSONResponse(
        content= {
            "singal": ResponseSignals.INSERT_INTO_VECTODB_SUCCESS.value,
            "inserted_items_count":inserted_items_count
        }
    )
@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request:Request, project_id:str):
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
        )
    project = await project_model.get_project_or_create_one(project_id= project_id)
    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
        )
    collection_info = nlp_controller.get_vector_db_collection_info(
         project=project
    )
    print(collection_info)
    
    return JSONResponse(
        content= {
            "singal": ResponseSignals.VECTOR_COLLECTION_RETRIVED.value,
            "collection_info":collection_info
        }
    )


@nlp_router.post("/index/search/{project_id}")
async def search_index(request:Request, project_id:str, search_request:SearchRequest):
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
        )
    project = await project_model.get_project_or_create_one(project_id= project_id)
    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
        )
    results = nlp_controller.search_vector_db_collection(project=project, 
                                                         text = search_request.text,
                                                          limit=search_request.limit )
    if not results:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
        content= {
            "singal": ResponseSignals.VECTORDB_SEARCH_ERROR.value,
            
        }
    )
    return JSONResponse(
        content= {
            "singal": ResponseSignals.VECTORDB_SEARCH_SUCCESS.value,
            "results":results
        }
    )
