"""Main entry point for pyspark jobs"""
import argparse
import importlib
import os
import sys

if os.path.exists("jobs.zip"):
    sys.path.insert(0, "jobs.zip")
else:
    sys.path.insert(0, "./jobs")

parser = argparse.ArgumentParser()
parser.add_argument("--job", type=str, required=True)
parser.add_argument("--jobtype", type=str, required=True)
parser.add_argument("--jobts", type=str, required=True)
args = parser.parse_args()

job_module = importlib.import_module(f"jobs.{args.jobtype}.{args.job}")
job_module.execute(args.jobts)
