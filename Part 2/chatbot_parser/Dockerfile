# Use an official Python runtime as an image
FROM python:3.8

EXPOSE 5050

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction
# creates a directory with this name if it doesn’t exist
WORKDIR /chatbot_parser

# Install any needed packages specified in requirements.txt
COPY requirements.txt /chatbot_parser
RUN pip install -r requirements.txt

# Run when the container launches
COPY chatbot_parser.py /chatbot_parser
CMD python chatbot_parser.py