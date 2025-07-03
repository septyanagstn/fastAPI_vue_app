from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import database
from bson import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "INI UJI COBA SAJA"}

@app.get("/articles/{source}")
async def get_all_articles(source: str):
    articles = await database[source].find().to_list(length=None)
    for article in articles:
        article["_id"] = str(article["_id"])
    return articles

@app.get("/articles/detail/{source}/{article_id}")
async def get_article_by_id(source: str, article_id: str):
    try:
        obj_id = ObjectId(article_id)
    except Exception:
        return {"error": "Invalid article_id format"}
    
    article = await database[source].find_one({"_id": obj_id})
    if article:
        article["_id"] = str(article["_id"])
        return article
    return {"error": "Article not found"}

@app.get("/articles/search/{query}")
async def search_articles(query: str):
    articles = []
    sources = ["kompas", "detik"]
    for source in sources:
        found_articles = await database[source].find({"title": {"$regex": query, "$options": "i"}}).to_list(length=None)
        for article in found_articles:
            article["_id"] = str(article["_id"])
            articles.append(article)
    return articles