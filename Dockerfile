# https://docs.docker.com/compose/django/
FROM python:3

# Define environment variable
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code
ADD . /code/

# Make port 80 available to the world outside this container
# EXPOSE 80

# Execute a shell directly
# https://docs.docker.com/engine/reference/builder/#cmd
CMD [ "sh", "-c", "echo $PYTHONUNBUFFERED" ]
