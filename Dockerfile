FROM python:3.9

# Install pipenv
RUN pip install pipenv

# Set the working directory
WORKDIR /workspace

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /workspace/

# Install dependencies
RUN pipenv install --dev

# Keep the container running
CMD ["tail", "-f", "/dev/null"]
