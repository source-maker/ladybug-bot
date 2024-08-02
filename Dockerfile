FROM python:3.9

COPY main.py /main.py

# install dependencies
RUN pip install requests

ENTRYPOINT ["python", "/main.py"]
