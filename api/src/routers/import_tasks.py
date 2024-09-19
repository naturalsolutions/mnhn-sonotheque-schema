from fastapi import APIRouter, BackgroundTasks
from uuid import uuid4
from src.tasks import import_workflows, sandbox, lazy_import_workflows, mds_import_workflows

router = APIRouter()


@router.get("/trigger-long-running-task")
async def trigger_long_running_task(background_tasks: BackgroundTasks):
    task_id = str(uuid4())
    background_tasks.add_task(sandbox.long_running_task.delay, task_id)
    return {"message": "Long-running task triggered", "task_id": task_id}

@router.get("/lazy-parse-seed-file")
async def lazy_parse_seed_file(background_tasks: BackgroundTasks):
    task_id = str(uuid4())
    background_tasks.add_task(lazy_import_workflows.lazy_process_import_file.delay)
    return {"message": "Lazy parse seed file with polars task triggered", "task_id": task_id}


@router.get("/parse-seed-file")
async def parse_seed_file(background_tasks: BackgroundTasks):
    task_id = str(uuid4())
    background_tasks.add_task(import_workflows.process_csv_file.delay)
    return {"message": "Long-running parsing task triggered", "task_id": task_id}

@router.get("/run-mds-import")
async def run_mds_import(background_tasks: BackgroundTasks):
    task_id = str(uuid4())
    background_tasks.add_task(mds_import_workflows.mds_process_csv_file.delay)
    return {"message": "Modern data stack parsing task triggered", "task_id": task_id}
