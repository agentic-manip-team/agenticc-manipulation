# ROS2 Dockerfile — ROS2 Humble + Python dependencies
FROM ros:humble

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    pydantic==2.5.2 \
    requests==2.31.0

# Copy ROS2 workspace code into the container
COPY ros2_ws /workspace/ros2_ws

# Source ROS2 setup on container start
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Default command
CMD ["bash"]