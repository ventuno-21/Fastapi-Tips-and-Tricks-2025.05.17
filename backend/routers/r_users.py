from fastapi import APIRouter


router = APIRouter()


@router.post("/register", description="Description of register function")
async def register():
    return {"message": "hi"}


@router.post("/login", description="Description of register function")
async def register():
    return {"message": "hi"}


@router.get("/", description="Description of register function")
async def get_user_profile():
    return {"message": "hi"}


@router.put("/", description="Description of register function")
async def get_update_profile():
    return {"message": "hi"}
