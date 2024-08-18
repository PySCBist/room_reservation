from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(title=settings.app_title, description=settings.description, lifespan=lifespan)

app.include_router(main_router)
