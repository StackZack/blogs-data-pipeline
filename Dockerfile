FROM apache/airflow:2.8.1-python3.11
COPY docker/airflow-requirements.txt /requirements.txt
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
