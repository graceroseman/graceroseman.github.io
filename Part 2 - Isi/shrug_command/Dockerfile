# Use an official Python runtime as an image
FROM python:3.8

EXPOSE 5051

# Sets the working directory for following COPY and CMD instructions
# Notice we haven't created a directory by this name - this instruction
# creates a directory with this name if it doesn't exist
WORKDIR /shrug_command

# Install any needed packages specified in requirements.txt
COPY . .
RUN pip install -r requirements.txt
CMD python shrug_command_server.py