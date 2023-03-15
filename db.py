from sqlalchemy import create_engine, Column, Integer, String, REAL
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///parsed_data.db')
Base = declarative_base()


class Data(Base):
    __tablename__ = 'profit_deals'
    id = Column(Integer, primary_key=True)
    from_token_symbol = Column(String(5))
    from_token_name = Column(String(50))
    from_token_address = Column(String(60))
    to_token_symbol = Column(String(5))
    to_token_name = Column(String(50))
    to_token_address = Column(String(60))
    aggregator = Column(String(15))
    price_USD = Column(Integer())
    final_price_with_gas_USD = Column(REAL())


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()