import os


os.environ['DATABASE_URL'] = 'postgresql://filex:files@localhost/files'

from main import app

app.run(debug=True)
