# instance/config.py

#Change the secret key by facerolling xd
SECRET_KEY = 'ffe7cb7cd2ed051bbb081ced0839a50e8ea2e0a22acf412a703c2e720865564cfcc86c9fe6f9571c89e96e3163'
# Use format mysql+pymysql://user:pass@<ip or hostname>/pycloudplatform
# Please make sure that the "pycloudplatform" database is created and the user has full access to the database
# SQLAlchemy would handle the database as needed
# The application expects pycloudplatform as the database name
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass:hostname/pycloudplatform'