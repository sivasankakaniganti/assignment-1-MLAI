FROM python:3.13

# Copy the contents of the app directory to /usr/src/app/
COPY src/ /usr/src/

# Set the working directory to /usr/src/app/
WORKDIR /usr/src/

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the application
CMD ["chainlit", "run", "app.py"]