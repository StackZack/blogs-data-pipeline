build:
	mkdir ./blog_airflow/dags/spark/dist
	cp ./blog_airflow/dags/spark/src/main.py ./blog_airflow/dags/spark/dist
	cd ./blog_airflow/dags/spark/src && zip -x main.py -r ../dist/jobs.zip .