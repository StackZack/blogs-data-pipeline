import argparse
import importlib
import os
import sys

import pyspark

if os.path.exists("jobs.zip"):
    sys.path.insert(0, "jobs.zip")
else:
    sys.path.insert(0, "./jobs")

parser = argparse.ArgumentParser()
parser.add_argument("--job", type=str, required=True)
parser.add_argument("--jobtype", type=str, required=True)
args = parser.parse_args()

sc = pyspark.SparkContext(appName=args.job)
job_module = importlib.import_module(f"jobs.{args.jobtype}.{args.job}")
job_module.execute(sc)
