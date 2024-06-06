import os
from taipy.gui import Gui
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def create_app():
    gui = Gui()
    return gui

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use the PORT environment variable or default to 5000
    app.run(title="webmecano", port=port)
