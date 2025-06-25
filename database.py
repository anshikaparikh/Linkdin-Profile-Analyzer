import sqlalchemy as db

engine = db.create_engine('sqlite:///profiles.db', connect_args={'check_same_thread': False})
metadata = db.MetaData()

profiles = db.Table('profiles', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('url', db.String()),
    db.Column('name', db.String()),
    db.Column('score', db.Integer()),
    db.Column('headline', db.String()),
    db.Column('about', db.String()),
)

metadata.create_all(engine)

def insert_profile(data):
    """Insert profile in a safe context"""
    with engine.connect() as conn:
        conn.execute(db.insert(profiles).values(data))
        conn.commit()

def get_profiles():
    """Get profiles in a safe context"""
    with engine.connect() as conn:
        result = conn.execute(db.select(profiles))
        return result.fetchall()

