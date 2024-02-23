build:
	mkdir -p ./blog_spark/dist
	cp ./blog_spark/src/main.py ./blog_spark/dist
	cd ./blog_spark/src && zip -x main.py -r ../dist/jobs.zip .