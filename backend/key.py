# cli.py
import secrets
import typer

app = typer.Typer()

@app.command()
def generate_key():
    key = secrets.token_hex(32)
    with open(".env", "a") as f:
        f.write(f"\nSECRET_KEY={key}")
    typer.echo("✅ Secret key generated and added to .env")

if __name__ == "__main__":
    app()