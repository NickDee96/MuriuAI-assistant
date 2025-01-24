# Use an official Python runtime as a parent image
FROM python:3.12.3

# Set the working directory in the container to /app
WORKDIR /app

# Add only the requirements.txt file first to leverage Docker cache
ADD requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add the rest of the application files
ADD . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000


# Run app.py when the container launches
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0"]
