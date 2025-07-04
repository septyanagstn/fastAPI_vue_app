from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from fastapi.security import OAuth2PasswordBearer
from database import database  
from bson import ObjectId
from passlib.context import CryptContext
from models import User, LoginUser, Token, Article  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

# SECRET_KEY = "rahasia-super-aman"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

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

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# Register
@app.post("/register/")
async def register(user: User = Body(...)):
    new_user = await database["users"].insert_one({
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "password": pwd_context.hash(user.password),
        "disabled": user.disabled
    })
    return {"message": "User registered successfully", "user_id": str(new_user.inserted_id)}

# Login
# @app.post("/login/", response_model=Token)
# async def login(user: LoginUser = Body(...)):
#     # Cari user di DB
#     user_data = await database["users"].find_one({"username": user.username})
#     if not user_data:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Verifikasi password
#     if not pwd_context.verify(user.password, user_data["password"]):
#         raise HTTPException(status_code=401, detail="Incorrect password")

#     # Buat token
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user_data["username"]},  # subject = username
#         expires_delta=access_token_expires
#     )

#     return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login/")
async def login(user: LoginUser = Body(...)):
    # Cek user berdasarkan email atau username
    user_data = await database["users"].find_one({
        "$or": [
            {"email": user.email},
            {"password": pwd_context.hash(user.password)}
        ]
    })

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verifikasi password
    if not pwd_context.verify(user.password, user_data["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    return {
        "message": "Login successful",
        "user": {
            "id": str(user_data["_id"]),
            "username": user_data["username"],
            "email": user_data["email"],
            "full_name": user_data["full_name"]
        }
    }
    
# Get all articles
@app.get("/articles/")
async def get_all_articles():
    articles = await database["kompas"].find().to_list(length=None)
    for article in articles:
        article["_id"] = str(article["_id"])
    return articles

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
    new_article = await database["test"].insert_one(
        article.model_dump(by_alias=True, exclude=["id"])
    )
    created_article = await database["test"].find_one(
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
        update_result = await database["test"].find_one_and_update(
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
    delete_result = await database["test"].delete_one({"_id": ObjectId(article_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Article deleted successfully", "article_id": article_id}
    return {"error": "Article not found"}

# Search articles by title
@app.get("/articles/search/{query}")
async def search_articles(query: str):
    articles = []
    found_articles = await database["kompas"].find({"title": {"$regex": query, "$options": "i"}}).to_list(length=None)
    for article in found_articles:
        article["_id"] = str(article["_id"])
        articles.append(article)
    return articles