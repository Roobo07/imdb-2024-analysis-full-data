from sqlalchemy import create_engine

def get_engine():
    username = "root"
    password = "password"
    host = "localhost"
    database = "imdb_2024"

    engine = create_engine(
        f"mysql+pymysql://{username}:{password}@{host}/{database}"
    )
    return engine
