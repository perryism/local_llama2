build:
	docker build . -t ll
run:
	# mount to local data folder
	docker run --rm --name ll -p 9999:8000 -v $(CURDIR)/data:/app/data ll
