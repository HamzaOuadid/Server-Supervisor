# Makefile for Linux

# Python executable
PYTHON := python3

# Virtual environment directory
VENV_DIR := .venv

# Main application script
APP_SCRIPT := dashapp.py

# Create a virtual environment and install dependencies
setup:
	(\
		${PYTHON} -m venv ${VENV_DIR}; \
		ls -la; \
		source ${VENV_DIR}/bin/activate; \
		echo "Installing dependencies..."; \
		pip install -r requirements.txt; \
		echo "Environment setup is complete."; \
	)

# Run the Streamlit application
run:
	echo "Running the Streamlit application...";
	streamlit run ${APP_SCRIPT};
	
# Remove virtual env
clean: 
	echo "> Removing virtual environment";
	rm -r ${VENV_DIR};

.PHONY: setup run
