# green-lambda
This project processes large TIF images by converting them to PNG format and splitting them into smaller, manageable chunks. 
It is designed to work in a serverless environment, triggered by events (e.g., file uploads to an S3 bucket),
 and processes images automatically by fetching, transforming, and saving the results.
 
# <span style="color: blue;">**Key Features:**</span>

# <sub>Image Conversion (TIF to PNG):</sub>


The ImageProcessor class handles the conversion of raster TIF images (with RGB bands) 
into PNG format using the rasterio and PIL libraries.

# <sub>Image Splitting:</sub>


The ImageProcessor class can split large PNG images into smaller chunks (tiles) of a specified size.
This is useful for processing or analyzing large datasets by breaking the image into smaller, more manageable pieces.
The chunks are saved as individual PNG files and the coordinates (offsets) of each chunk within the original image are tracked and stored.

# <sub>Serverless Image Handling:</sub>


The ImageHandler class processes events triggered by image uploads to an S3 bucket.
The handler function is the main entry point and calls the ImageHandler to perform the image processing tasks, 
which include fetching, converting, splitting, and uploading the processed files back to S3.

# <sub>Helper Functions:</sub>


- Metadata Extraction: Metadata associated with the image can be extracted and saved. <br>
- Offsets Handling: Tracks the positions of image chunks to enable the reassembly of the original image later if needed.<br>
- File Uploading: Once processed, the image chunks, metadata, and offsets are uploaded back to an S3 bucket.<br>

# <span style="color: blue;">**Workflow:**</span>

- An image is uploaded to an S3 bucket.
- The handler function is triggered by the upload event, calling the ImageHandler to fetch the image, process it (convert and split), and upload the results back to S3.
- The process includes:
   - Converting the TIF image to PNG.
   - Splitting the PNG into smaller chunks.
   - Extracting metadata and offsets.
   - Uploading the processed chunks, metadata, and offsets back to the S3 bucket.
   

# <span style="color: blue;">**Requirements:**</span>
  - Python 3.10
  - Libraries: numpy, PIL, rasterio
  - AWS S3 bucket (for file storage and triggering the process)   
  

# <span style="color: blue;">**Usage:**</span>
 - Set up your S3 bucket to trigger the handler function whenever a new image is uploaded.
 - The ImageHandler class automatically fetches the image, processes it, and uploads the results (image chunks, metadata, and offsets) back to S3.  

# <span style="color: blue;">**Docker Integration:**</span>

This project is packaged in Docker and uploaded to AWS Lambda as a Docker image through Amazon Elastic Container Registry (ECR). Docker allows the entire project, 
including its dependencies and environment, to be easily managed and deployed within AWS Lambda, ensuring consistent execution in a serverless environment.

This project enables efficient processing of large image files, converting them into manageable pieces and providing metadata and chunk offsets for further processing or analysis.


 
