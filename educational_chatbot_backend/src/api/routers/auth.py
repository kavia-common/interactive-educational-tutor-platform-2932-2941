from fastapi import APIRouter, Depends, HTTPException, status
from ..models.schemas import SignupRequest, LoginRequest, TokenResponse
from ..db.deps import get_db
from ..db.interface import DatabaseInterface
from ..services import auth_service

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "/signup",
    summary="User Signup",
    description="Create a new user and return access token.",
    response_model=TokenResponse,
    responses={
        201: {"description": "User created"},
        400: {"description": "User already exists"},
    },
)
def signup(payload: SignupRequest, db: DatabaseInterface = Depends(get_db)):
    """Create a user and issue an access token."""
    try:
        result = auth_service.signup(db, email=payload.email, password=payload.password, name=payload.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"access_token": result["token"], "token_type": "bearer", "expires_in": 60 * 60}


# PUBLIC_INTERFACE
@router.post(
    "/login",
    summary="User Login",
    description="Authenticate and return access token.",
    response_model=TokenResponse,
    responses={
        200: {"description": "Authenticated"},
        401: {"description": "Invalid credentials"},
    },
)
def login(payload: LoginRequest, db: DatabaseInterface = Depends(get_db)):
    """Authenticate a user and return a token."""
    try:
        result = auth_service.login(db, email=payload.email, password=payload.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return {"access_token": result["token"], "token_type": "bearer", "expires_in": 60 * 60}
