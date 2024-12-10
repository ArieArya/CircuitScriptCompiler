FROM ubuntu:22.04

# Update and install dependencies.
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    ninja-build

# Install Meson.
RUN pip3 install meson

# Set working directory.
WORKDIR /app

# Copy project files.
COPY . .

# Build VM.
RUN cd vm && \
    meson setup --wipe build && \
    cd build && \
    ninja

# Run scripts.
# Cannot have multiple CMDs, so we make this one a RUN.
RUN python3 run_compiler.py
CMD ["python3", "run_vm.py"]
