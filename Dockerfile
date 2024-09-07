# Use the python3.10.13 base image
FROM python:3.10.13

# Set environment variable to prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

# Create a directory named 'pms-be' in the container
RUN mkdir /pms-be

# Set working directory to '/pms-be' in the container
WORKDIR /pms-be

# Copy only the requirements file to leverage Docker caching
COPY requirements.txt /pms-be/

# Create a Python virtual environment named 'venv'
RUN python -m venv venv

# Activate the virtual environment ('.' runs the activate script within the shell, but in Docker, each RUN command starts a new shell, so activation won't persist)
RUN . venv/bin/activate

# Copy the rest of the project files into the '/pms-be' directory in the container
COPY . /pms-be/
