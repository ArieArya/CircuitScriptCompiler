# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy Python scripts into the container
COPY tokenizer.py tester.py dfa.py .

# Copy sample_code directory into the container
COPY sample_code/ sample_code/

# Run script
CMD ["python", "tester.py"]