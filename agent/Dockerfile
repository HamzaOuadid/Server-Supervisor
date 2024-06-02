FROM python:3.10-slim

# adding make
RUN apt update && apt install -y make

# configure docker to run in the current dir
WORKDIR /agent

# copy requirement files inside the container
COPY Makefile /agent/Makefile
COPY requirements.txt /agent/requirements.txt
COPY requirements.dev.txt /agent/requirements.dev.txt

# install the requirements in venv
RUN make environment

# copy agent code
COPY . /agent

# expose port 8000 of the container
EXPOSE 8000

# run the agent
CMD ["make", "run"]
