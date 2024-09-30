import time
from fastapi import Request, Response, status

from models import Watch
from sqlmodel import select

from . import app
from .deps import SessionDep
from .metrics import metrics


@app.middleware("http")
async def request_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    metrics.requests_metric.labels(
        method=request.method,
        path=request.url.path,
        status=response.status_code
    ).inc()
    metrics.request_histogram_metric.labels(
        method=request.method,
        path=request.url.path,
        status=response.status_code,
    ).observe(process_time)
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/metrics")
def read_metrics():
    data = metrics.get()
    return Response(content=data, media_type="text/plain; version=0.0.4; charset=utf-8")


@app.get("/healthz")
def read_healthz():
    return {"status": "ok"}


@app.get("/forecaster/v1/watch", response_model=list[Watch])
def get_watches(session: SessionDep):
    watched_metrics = session.exec(select(Watch)).all()
    return watched_metrics


@app.get("/forecaster/v1/watch/{watch_id}")
def get_watch(session: SessionDep, watch_id: int):
    return session.get(Watch, watch_id)


@app.put("/forecaster/v1/watch/{watch_id}")
def put_watch(session: SessionDep, watch_id: int, watch_update: Watch):
    watch = session.get(Watch, watch_id)
    watch.sqlmodel_update(watch_update.model_dump(exclude_unset=True))
    session.add(watch)
    session.commit()
    session.refresh(watch)
    return watch


@app.post("/forecaster/v1/watch")
def post_watch(session: SessionDep, watch: Watch, response: Response):
    db_watch = Watch.model_validate(watch)
    session.add(db_watch)
    session.commit()
    session.refresh(db_watch)
    response.status_code = status.HTTP_201_CREATED
    return db_watch


@app.delete("/forecaster/v1/watch/{watch_id}")
def delete_watch(session: SessionDep, watch_id: int):
    db_watch = session.get(Watch, watch_id)
    db_watch.delete()
    session.add(db_watch)
    session.commit()
    return {"status": "ok"}
