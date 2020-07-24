import datetime
import logging
import os
import uuid

import azure.functions as func
from pybaseball import statcast
import pymysql  # noqa: F401
from sqlalchemy import create_engine

engine = create_engine(os.environ["MYSQL_STATCAST"], pool_pre_ping=True)


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = (
        datetime.datetime.utcnow()
        .replace(tzinfo=datetime.timezone.utc)
        .isoformat()  # noqa: E501
    )

    if mytimer.past_due:
        logging.info("The timer is past due!")

    start_dt = (datetime.date.today() - datetime.timedelta(1)).strftime(
        "%Y-%m-%d"
    )  # noqa: E501
    end_dt = start_dt  # pull yesterday's statcast data
    schema = "pitchbypitch"

    df = statcast(start_dt=start_dt, end_dt=end_dt,)
    logging.info(f"Ran statcast(start_dt={start_dt}, end_dt={end_dt})")

    df["id"] = df.apply(lambda row: uuid.uuid1(), axis=1).astype(str)

    df.to_sql(schema, engine, if_exists="append", index=False)
    logging.info(f"Added {len(df.index)} rows to {schema} at {utc_timestamp}")
