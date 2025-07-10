from database.db import engine, Base
from database import models

Base.metadata.create_all(bind=engine)
print("Base de datos y tablas creadas correctamente.")
