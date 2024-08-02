FROM python:3.9

COPY main.py /main.py

ENTRYPOINT ["python", "/main.py"]
