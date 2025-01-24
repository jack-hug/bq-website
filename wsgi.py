from bqwebsite import create_app
from dotenv import load_dotenv


app = create_app()

if __name__ == "__main__":
    app.run()
