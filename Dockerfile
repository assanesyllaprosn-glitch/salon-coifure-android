FROM ubuntu:20.04

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3 \
    python3-dev \
    openjdk-8-jdk \
    libc6-dev-i386 \
    lib32z1 \
    lib32ncurses5 \
    libstdc++6 \
    zlib1g-dev \
    libncurses5-dev \
    libtinfo5 \
    libbz2-1.0 \
    automake \
    libtool \
    pkg-config \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python pip and buildozer
RUN pip3 install buildozer cython

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Build APK
RUN buildozer android debug

# Copy APK to output directory
RUN mkdir -p /output && cp bin/*.apk /output/
