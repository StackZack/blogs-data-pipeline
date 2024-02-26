build:
	mkdir -p ./blog_spark/dist
	cp ./blog_spark/src/main.py ./blog_spark/dist
	cd ./blog_spark/src && zip -x main.py -x \*libs\* -r ../dist/jobs.zip .
	cd ./blog_spark/src/libs && zip -r ../../dist/libs.zip .
