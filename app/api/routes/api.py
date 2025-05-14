from fastapi import APIRouter

router = APIRouter()


@router.get("/projects")
async def fetch_projects():
    return {"message": "Hello World"}
