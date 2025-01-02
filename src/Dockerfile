# Use the Amazon Linux 2 base image
FROM public.ecr.aws/lambda/python:3.10

# Install Python 3.12, development tools, and system dependencies for rasterio
RUN yum update -y && \
    yum install -y \
    gcc \
    gdal-devel \
    proj-devel \
    expat-devel \
    python3 \
    python3-devel \
    make \
    libcurl-devel \
    python3-pip \
    && yum clean all

# Set the working directory to /var/task (default for Lambda)
#WORKDIR /var/task

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies using pip3
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy function code to container
#COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY config.py ${LAMBDA_TASK_ROOT}
COPY s3_uploader.py ${LAMBDA_TASK_ROOT}
COPY metadata_handler.py ${LAMBDA_TASK_ROOT}
COPY offsets_handler.py ${LAMBDA_TASK_ROOT}
COPY image_handler.py ${LAMBDA_TASK_ROOT}
COPY image_processor.py ${LAMBDA_TASK_ROOT}

# setting the CMD to your handler file_name.function_name
CMD ["lambda_function.handler"]



