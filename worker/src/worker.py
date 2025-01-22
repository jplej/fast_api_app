from celery import Celery

celery_worker = Celery(
    "celery_worker",
    broker="redis://redis:6379/0",  # Redis broker
    backend="redis://redis:6379/0"  # Optional: Redis backend for results
)

# Add the new `add` task to the process map
def add(numbers):
    print(f"Adding numbers: {numbers}")
    return sum(numbers)

PROCESS_MAP = {
    "add": add,  # Add the new task here
}

@celery_worker.task(name="handle_task")
def handle_task(task_data):
    process_name = task_data.get("process_name")
    data = task_data.get("data")

    if process_name not in PROCESS_MAP:
        raise ValueError(f"Unknown process_name: {process_name}")

    # Call the appropriate function and return the result
    return PROCESS_MAP[process_name](data)


