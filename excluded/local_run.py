import os

from src.main import app

os.system("export APP_SETTINGS='config.DevelopmentConfig'")
os.system('export DATABASE_URL="postgresql://localhost/files"')

app.run(debug = True)
