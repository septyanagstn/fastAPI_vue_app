# FastAPI Vue APP

Eksplorasi web application menggunakan FastAPI sebagai Backend dan Vue.js sebagai Frontend...

## Tech Stack

**Backend:** Python, FastAPI

**Frontend:** Node, Vue.js

**Database:** MongoDB

## Run Locally

Clone the project

```bash
  git clone https://github.com/septyanagstn/fastAPI_vue_app.git
```

### Backend

Go to the Backend project directory

```bash
  cd backend
```

Install dependencies

```bash
  pip install -r requirements.txt
```

#### Set Environtment Variable

Set the `.env` variable

```bash
  cp .env.example .env
```

generate secret key and copy to `.env`

```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Customize the token validity period according to your needs

```bash
  ACCESS_TOKEN_EXPIRE_MINUTES= "set your duration"
```

#### Set up database

Go to `database.py` file and change database name with yours

```bash
  database = client["your_database"]
```

#### Start the server

```bash
  uvicorn main:app --reload
```

### Frontend

Go to the Frontend project directory

```bash
  cd frontend
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run dev
```
## Screenshots

![Screenshot 1](/assets/login.png) | ![Screenshot 2](/assets/register.png) | ![Screenshot 3](/assets/dasbor.png) |
|------------------------------------------|------------------------------------------|------------------------------------------|
| ![Screenshot 4](/assets/detail.png) | ![Screenshot 5](/assets/list-article.png) | ![Screenshot 6](/assets/list-user.png) |

## Authors

- [@septyanagstn](https://www.instagram.com/septyanagstn)