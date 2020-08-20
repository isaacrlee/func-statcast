import logging
import os
import uuid

import azure.functions as func
from pybaseball import statcast
import pymysql  # noqa: F401
from sqlalchemy import create_engine

engine = create_engine(os.environ["MYSQL_STATCAST"], pool_pre_ping=True)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    start_dt = req.params.get("start_dt")
    if not start_dt:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            start_dt = req_body.get("start_dt")

    end_dt = req.params.get("end_dt")
    if not end_dt:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            end_dt = req_body.get("end_dt")

    if not start_dt or not end_dt:
        return func.HttpResponse(
            "Please pass start_dt and end_dt on the query string or in the request body",
            status_code=400,
        )

    schema = "pitchbypitch"

    df = statcast(start_dt=start_dt, end_dt=end_dt)
    logging.info(f"Ran statcast(start_dt={start_dt}, end_dt={end_dt})")

    df["id"] = df.apply(lambda row: uuid.uuid1(), axis=1).astype(str)

    df.to_sql(schema, engine, if_exists="append", index=False)
    logging.info(f"Added {len(df.index)} rows to {schema}")

    return func.HttpResponse(df.to_json(orient="records"))
