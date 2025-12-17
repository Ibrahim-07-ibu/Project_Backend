from fastapi import FastAPI
from db.database import Base, engine
from routers import users,bookings,provider_services,providers,reviews,services,supports

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(provider_services.router)
app.include_router(providers.router)
app.include_router(reviews.router)
app.include_router(services.router)
app.include_router(supports.router)
@app.get("/")
def greet():
    return {"message": "Home Buddy API Running"}
