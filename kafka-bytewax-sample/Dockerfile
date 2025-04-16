# Start from a debian slim with python support
FROM python:3.12-slim-bullseye
# Set up a workdir where we can put our dataflow
WORKDIR /bytewax
# Install bytewax and the dependencies you need here
COPY requirements.txt requirements.txt 
RUN python -m pip install -r requirements.txt

# Copy the dataflow in the workdir
COPY businesslogic businesslogic
COPY myflow.py myflow.py
COPY .env .env

# And run it.
# Set PYTHONUNBUFFERED to any value to make python flush stdout,
# or you risk not seeing any output from your python scripts.
ENV PYTHONUNBUFFERED 1
CMD ["python", "-m", "bytewax.run", "myflow"]