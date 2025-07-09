from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from database import database  
from bson import ObjectId
from passlib.context import CryptContext
from models import User, LoginUser, Article  
import os
from dotenv import load_dotenv
from fastapi import Query
import jwt

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/")
async def root():
    return {"message": "Halo Brader"}

# Create access token with time expire
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Register  
@app.post("/register/")
async def register(user: User = Body(...)):
    existing_user = await database["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = await database["users"].insert_one({
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "password": pwd_context.hash(user.password),
        "disabled": user.disabled
    })
    return {"message": "User registered successfully", "user_id": str(new_user.inserted_id)}

# Login and create new access token
@app.post("/login/")
async def login(user: LoginUser = Body(...)):
    user_data = await database["users"].find_one({
        "email": user.email
    })

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not pwd_context.verify(user.password, user_data["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data["username"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user_data["_id"]),
            "username": user_data["username"],
            "email": user_data["email"],
            "full_name": user_data["full_name"]
        }
    }

# Get Users
@app.get("/users/")
async def get_users(skip: int = Query(0), limit: int = Query(10)):
    total_users = await database["users"].count_documents({})

    users = await database["users"].find().sort("username", 1).skip(skip).limit(limit).to_list(length=limit)
    for user in users:
        user["_id"] = str(user["_id"])

    return {
        "items": users,
        "total": total_users
    }

# Create User
@app.post("/users/")
async def create_user(user: User = Body(...)):
    existing_user = await database["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = await database["users"].insert_one({
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "password": pwd_context.hash(user.password),
        "disabled": user.disabled
    })
    return {"message": "User created successfully", "user": new_user}

# get User by ID
@app.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    try:
        obj_id = ObjectId(user_id)
    except Exception:
        return {"error": "Invalid user_id format"}
    
    user = await database["users"].find_one({"_id": obj_id})
    if user:
        user["_id"] = str(user["_id"])
        return user
    return {"error": "User not found"}

# Update user by ID
@app.put("/users/{user_id}")
async def update_user_by_id(user_id: str, user: User = Body(...)):
    user = user.model_dump(by_alias=True)

    existing_user = await database["users"].find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        return {"error": "User not found"}
    
    # Jika password tidak kosong, hash password
    if user.get("password") and user.get("password") != existing_user.get("password"): 
        user["password"] = pwd_context.hash(user["password"])

    # Hapus field kosong (None)
    update_fields = {k: v for k, v in user.items() if v is not None}

    if len(user) >= 1:
        update_result = await database["users"].find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_fields}
        )

        if update_result is not None:
            update_result["_id"] = str(update_result["_id"])
            return {"message": "User updated successfully", "user": update_result}
        return {"error": "User not found"}
    return {"error": "No fields to update"}

# Delete user by ID
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    delete_result = await database["users"].delete_one({"_id": ObjectId(user_id)})
    if delete_result.deleted_count == 1:
        return {"message": "User deleted successfully", "user_id": user_id}
    return {"error": "User not found"}

# Search users by username
@app.get("/users/search/{query}")
async def search_users(query: str, skip: int = 0, limit: int = 10):
    filter_query = {"username": {"$regex": query, "$options": "i"}}

    total_users = await database["users"].count_documents(filter_query)
    found_users = await database["users"].find(filter_query).sort("post_date", -1).skip(skip).limit(limit).to_list(length=limit)

    for user in found_users:
        user["_id"] = str(user["_id"])

    return {
        "items": found_users,
        "total": total_users
    }

# Get all articles
@app.get("/articles/")
async def get_articles(skip: int = Query(0), limit: int = Query(10)):
    total_articles = await database["kompas"].count_documents({})

    articles = await database["kompas"].find().sort("post_date", -1).skip(skip).limit(limit).to_list(length=limit)
    for article in articles:
        article["_id"] = str(article["_id"])

    return {
        "items": articles,
        "total": total_articles
    }

# Get detail article by ID
@app.get("/articles/detail/{article_id}")
async def get_article_by_id(article_id: str):
    try:
        obj_id = ObjectId(article_id)
    except Exception:
        return {"error": "Invalid article_id format"}
    
    article = await database["kompas"].find_one({"_id": obj_id})
    if article:
        article["_id"] = str(article["_id"])
        return article
    return {"error": "Article not found"}

# Create a new article
@app.post("/articles/")
async def create_article(article: Article = Body(...)):
    new_article = await database["kompas"].insert_one(
        article.model_dump(by_alias=True, exclude=["id"])
    )
    created_article = await database["kompas"].find_one(
        {"_id": new_article.inserted_id}
    )
    if created_article:
        created_article["_id"] = str(created_article["_id"])
    return {"message": "Article created successfully", "article": created_article}

# Update article by ID
@app.put("/articles/{article_id}")
async def update_article_by_id(article_id: str, article: Article = Body(...)):
    article = {
        k: v for k, v in article.model_dump(by_alias=True).items() if v is not None
    }

    if len(article) >= 1:
        update_result = await database["kompas"].find_one_and_update(
            {"_id": ObjectId(article_id)},
            {"$set": article}
        )

        if update_result is not None:
            update_result["_id"] = str(update_result["_id"])
            return {"message": "Article updated successfully", "article": update_result}
        return {"error": "Article not found"}
    return {"error": "No fields to update"}

# Delete article by ID
@app.delete("/articles/{article_id}")
async def delete_article(article_id: str):
    delete_result = await database["kompas"].delete_one({"_id": ObjectId(article_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Article deleted successfully", "article_id": article_id}
    return {"error": "Article not found"}

# Search articles by title
@app.get("/articles/search/{query}")
async def search_articles(query: str, skip: int = 0, limit: int = 10):
    filter_query = {"title": {"$regex": query, "$options": "i"}}

    total_articles = await database["kompas"].count_documents(filter_query)
    found_articles = await database["kompas"].find(filter_query).sort("post_date", -1).skip(skip).limit(limit).to_list(length=limit)

    for article in found_articles:
        article["_id"] = str(article["_id"])

    return {
        "items": found_articles,
        "total": total_articles
    }