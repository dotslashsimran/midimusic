FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    fluidsynth libfluidsynth2 libfluidsynth-dev \
    ffmpeg \
    && pip install flask pillow midiutil

# Set work directory
WORKDIR /app
COPY . .

# Set the entrypoint
CMD ["python", "app.py"]