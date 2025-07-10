from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.vuln_scan import Base  # Importa Base y tus modelos aquí

# Cambia USER, PASSWORD, HOST, PORT y DBNAME por los valores correctos
DATABASE_URL = "mysql+pymysql://root:abcd*1234@127.0.0.1:3306/cyberdashboard?charset=utf8mb4"


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # útil para mantener viva la conexión
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
