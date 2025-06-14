from fastapi import FastAPI
from contextlib import asynccontextmanager
from routs import base, data, nlp
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Code to run on startup
    await startup_span()

    yield

    # ✅ Code to run on shutdown (optional)
    await shutdown_span()

app = FastAPI(lifespan=lifespan)




async def startup_span():
    settings = get_settings()
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGREST_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    app.db_engine = create_async_engine(postgres_conn)

    app.db_client = sessionmaker(
        app.db_engine, class_ = AsyncSession, expire_on_commit=False,
    )

    llm_provider_factory = LLMProviderFactory(settings)

    vectordb_provider_factory = VectorDBProviderFactory(config=settings, db_client=app.db_client)


    #generation client
    app.generation_client = llm_provider_factory.create(provider = settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)
    #embedding client
    app.embedding_client =  llm_provider_factory.create(provider = settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id = settings.EMBEDDING_MODEL_ID,embedding_size = settings.EMBEDDING_MODEL_SIZE)

    #vectordb client
    app.vectordb_client = vectordb_provider_factory.create(settings.VECTOR_DB_BACKEND)


    await app.vectordb_client.connect()
    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG
        )




async def shutdown_span():
    app.db_engine.dispose()
    await app.vectordb_client.disconnect()

# app.router.lifespan.on_startup.append(startup_span)
# app.router.lifespan.on_shutdown.append(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)