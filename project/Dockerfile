# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11

# Copy local code to the container image.
WORKDIR /app

# Copy the contents of the project folder to the container at /app
COPY . .

# Install production dependencies.
RUN pip install -r requirements.txt

EXPOSE 8080


CMD python src/app.py