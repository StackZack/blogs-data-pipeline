FROM alpine:3.19.1 AS builder

# Install build related dependencies
RUN apk add zip --no-cache make

# Copy source code and build file to builder
COPY blog_spark blog_spark
COPY Makefile Makefile

# Build source code
RUN make build

FROM apache/airflow:2.8.1-python3.11

# Install dependencies needed for spark
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-17-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
# TODO: Make dockerfile arch independent
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64

# Copy build artifacts
COPY --from=builder /blog_spark/dist /opt/airflow/spark/dist
# Copy requirements to install additional dependencies
COPY docker/airflow/requirements.txt /requirements.txt
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
