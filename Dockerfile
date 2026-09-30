# start from a lightweight version of python
FROM python:3.11-slim

# set the working folder inside the container
WORKDIR /app

# copy the requirements file in first and install the packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the app's files into the container
COPY . .

# start the app when the container runs, using the port cloud run assigns
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
