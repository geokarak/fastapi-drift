.PHONY: fastdrift-start
fastdrift-start:
	uvicorn src.fastdrift.app:app --port 8000 --reload

.PHONY: locust-start
locust-start:
	cd ./src/fastdrift && locust -f locust.py