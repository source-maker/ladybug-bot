FROM python:3.9

# 明示しておく
ENTRYPOINT ["/bin/bash", "-c"]

# Install pipenv
RUN pip install pipenv

# Set the working directory
WORKDIR /workspace

# Copy the Pipfile and Pipfile.lock to the container
ADD . /workspace

# Install dependencies
RUN pipenv install --system --dev

# Keep the container running
CMD ["tail", "-f", "/dev/null"]
