FROM python:3.10-slim

# adding make
RUN apt update && apt install -y make

# configure docker to run in the current dir
WORKDIR /Dashboard

# copy requirement files inside the container
COPY ./Makefile /Dashboard/Makefile
COPY ./requirements.txt /Dashboard/requirements.txt

# copy dashboard code
COPY . /Dashboard

# install the requirements in venv
RUN make setup

# expose port 8501 of the container
EXPOSE 8501

# run the agent
CMD ["make", "run"]
