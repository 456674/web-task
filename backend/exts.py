from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from flask_cors import CORS

import config
import app

# db = SQLAlchemy(config.SQLALCHEMY_DATABASE_URI)
cors = CORS()