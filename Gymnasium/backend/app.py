from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, schools, users

app = FastAPI(
    title="Gymnasium API",
    description="API for Gymnasium school predictions and information",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8006",
        "http://localhost:3000",
        "https://gymnasium.edigistay.com",
        "https://gymnasium.jhaavinash.in"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(schools.router, prefix="/api", tags=["Schools"])
app.include_router(users.router, prefix="/api", tags=["Users"])

@app.get("/health")
async def health_check():
    return "OK" 