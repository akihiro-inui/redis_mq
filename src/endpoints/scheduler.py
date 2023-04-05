import os
import sys

sys.path.insert(0, os.getcwd())

from redis import exceptions
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
from src.utils.custom_error_handlers import RedisError
from src.utils.types import RegisterJobRequest
from src.scheduler.worker import CustomWorker
from src.scheduler import MQ, queue


router = APIRouter()


@router.post("/register_job")
async def register_job(input_array: RegisterJobRequest) -> JSONResponse:
    """
    Async function to enqueue the job to the message queue.
    and return the result to let client knows the job is queued.
    :param input_array: Input unsorted integer array from the client
    :return: Json response that contains the success status of queuing the job.
    """
    # Queue the job
    try:
        result = MQ.enqueue_job(queue, CustomWorker.create_job, input_array)
        job_id = result.get_id()
        return JSONResponse(
            status_code=201,
            content=dict(
                status="OK",
                message="Successfully enqueued the job",
                job_id=job_id,
            ),
        )

    # Thrown an error if connection to Redis fails
    except exceptions.ConnectionError:
        raise RedisError(
            status_code=500,
            message="Failed to enqueued the job. Check Redis is running and ready to accept the connection",
        )


@router.get("/jobs/{job_id}")
def get_job_status(job_id: str) -> JSONResponse:
    """
    Given the job ID, retrieve the job status and the result if it's finished
    :param job_id: Job ID to query the status and the result
    :return: Json response that contains the job ID, status, enqueued_at (timestamptz), duration and sorted array
    """
    try:
        # Fetch job status by its ID
        job_status = MQ.get_job_status(queue, job_id)
    # Throw the error if connection to Redis fails
    except exceptions.ConnectionError:
        raise RedisError(
            status_code=500,
            message="Failed to enqueued the job. Check Redis is running and ready to accept the connection",
        )

    # If no job result, the provided job ID does not exist
    if not job_status:
        return JSONResponse(
            status_code=400,
            content=dict(
                message="Requested job does not exist. Either wrong job ID or it was wiped from DB",
                job_id=job_id,
            ),
        )
    # Get job status
    job_status_name = job_status._status
    job_metadata = job_status.to_dict()

    # If the job is retrieved, create metadata and send it back
    payload = dict(
        message="Successfully retrieved the requested job status",
        job_id=job_id,
        job_status=job_status_name,
        result=[],
        enqueued_at=job_metadata["enqueued_at"],
        duration="",
    )
    if job_status_name == "finished":
        payload["result"] = job_status.result
        payload["duration"] = str(
            datetime.strptime(job_metadata["ended_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
            - datetime.strptime(job_metadata["started_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
        )
    return JSONResponse(status_code=200, content=payload)


@router.get("/jobs")
def get_all_jobs_status() -> JSONResponse:
    """
    Get all jobs that are; queued, failed and finished
    and return the them as list of dictionary e.g. [{"job_id": UUID, "status": "finished"}]
    :return: Json response that contains the list of the jobs and their status
    """
    try:
        # Get all jobs and their status
        all_jobs = MQ.get_all_job_status(queue)
    except exceptions.ConnectionError:
        raise RedisError(
            status_code=500,
            message="Failed to enqueued the job. Check Redis is running and ready to accept the connection",
        )

    # Return all jobs and their status
    return JSONResponse(
        status_code=200,
        content=dict(message="Successfully retrieved all jobs status", jobs=all_jobs),
    )
