# Base Python image
FROM python:3.8

EXPOSE 5555

COPY src src
COPY setup.cfg setup.cfg
COPY setup.py setup.py


# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -e .[all]

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:5555/status || exit 1

# Run API server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5555"]
