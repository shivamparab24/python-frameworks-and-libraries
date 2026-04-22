from fastapi import FastAPI
from FastAPI.Ssali_Jonathan.CRUD.auth.auth_router import auth_router
from FastAPI.Ssali_Jonathan.CRUD.books.book_router import book_router
from FastAPI.Ssali_Jonathan.CRUD.core.middleware import register_middleware
from FastAPI.Ssali_Jonathan.CRUD.reviews.review_router import review_router
from FastAPI.Ssali_Jonathan.CRUD.tags.tags_routes import tags_router
from FastAPI.Ssali_Jonathan.CRUD.core.errors import register_all_errors
from FastAPI.Ssali_Jonathan.CRUD.core.database import init_db


from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting...")
    await init_db()
    yield
    print(f"server has stopper!!")


version = "v1"


app = FastAPI(
    version=version,
    title="Booky",
    description="RestAPI for Book Review",
    lifespan=life_span,
    redoc_url=f"/api/{version}/redoc"
)

register_all_errors(app)

register_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["Tags"])