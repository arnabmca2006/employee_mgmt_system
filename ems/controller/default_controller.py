from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    response_model=str,
    summary="Fetch the status of the service",
    description="Fetch the status of the service.",
    responses={
        200: {"description": "OK - Successfully returns status"},
        "default": {"description": "Internal Server Error"}
    }
)
def status():
    return "Status: Ok"
