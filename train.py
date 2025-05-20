# Importing necessary modules from Azure SDK and Python standard libraries
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient  # Client to access Custom Vision Training API
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, ImageFileCreateBatch  # Models to upload image files in batches
from msrest.authentication import ApiKeyCredentials  # Handles API key authentication for Azure SDK
import os  # Provides functions to interact with the operating system (like file and folder navigation)
from logger import logger  # Custom logger module for logging messages to a file or console
from exception import CustomException  # Custom exception class for structured error handling
import time  # Used to delay loop execution (sleep), useful for checking training status repeatedly


# Saving credentials and model-related configuration
endpoint = "https://automobiletraining.cognitiveservices.azure.com/"  # Azure endpoint for your Custom Vision resource
api_key1_training = "FLaCIQL2b83tQjKSqmOsYpTl3pIFQUffh7ciVNIvuPUKQ35gII6MJQQJ99BEACGhslBXJ3w3AAAJACOGuNew"  # Training key for authentication
resource_id_prediction = "/subscriptions/7e799c2d-1d5c-44ef-ba1f-9af09461a72c/resourceGroups/azureservices102/providers/Microsoft.CognitiveServices/accounts/automobilePrediction"
# Azure resource ID for prediction endpoint
project_name = "carBrandtraining"  # Name of the Custom Vision project to be created
publish_iteration_name = "car_brand_model_v1"  # Name under which the trained model will be published


# Authenticate the client using the training key
try:
    logger.info("Authenticating API - ENDPOINT")
    credentials = ApiKeyCredentials(in_headers={"Training-key": api_key1_training})  # Create credential object
    trainer = CustomVisionTrainingClient(endpoint, credentials)  # Initialize the training client
except Exception as e:
    logger.error(e)
    raise CustomException(e)  # Handle and raise any authentication failure


# List all available domains in Azure Custom Vision (used for defining the type of problem e.g. classification)
domains = trainer.get_domains()
for domain in domains:
    print(f"Name: {domain.name}, ID: {domain.id}, Type: {domain.type}, Exportable: {domain.exportable}")  # Print details for each domain


# Select the "General (compact)" domain specifically suited for multiclass classification and allows model export
logger.info("Getting domain for classification")
domain = next(domain for domain in trainer.get_domains()
              if domain.type == "Classification" and domain.name == "General (compact)")
logger.info(f"Domain [{domain.name}] selected with ID [{domain.id}]")


# Create a new project in Custom Vision
logger.info("Initializing Project Name")
project = trainer.create_project(
    name=project_name,  # The name given to the new project
    classification_type="Multiclass",  # Specifies this is a multiclass problem (one label per image)
    domain_id=domain.id,  # Use the selected domain ID
    description="Multi-class classifier for car brands"  # Optional project description
)
logger.info("Project Name created successfully")


# Define the path to the training dataset and initialize a dictionary for tags
image_folder_path = "train set"  # Root folder containing subfolders named after car brands
tags_map = {}  # Dictionary to map brand name to tag object
logger.info("Database Initiated")


# Print folder names inside the dataset path (typically brand names)
for imgdir in os.listdir(image_folder_path):
    print(imgdir)


# Assign tags for each brand (subfolder) and upload images to the project
try:
    for folder in os.listdir(image_folder_path):  # Loop through each brand folder
        folder_path = os.path.join(image_folder_path, folder)  # Build full folder path

        if os.path.isdir(folder_path):  # Ensure it's a folder
            tag = trainer.create_tag(project.id, folder)  # Create a tag with the folder (brand) name
            tags_map[folder] = tag  # Store tag in dictionary
            logger.info(f"Tags created for folder {folder}")

        for image_file in os.listdir(folder_path):  # Loop through each image in the brand folder
            image_path = os.path.join(folder_path, image_file)  # Full path to image
            with open(image_path, "rb") as img_data:  # Open image in binary mode
                try:
                    logger.info(f"Uploading  {image_file}....given tag {folder}....path {image_path}")
                    entry = ImageFileCreateEntry(
                        name=image_file,  # Name of the image file
                        contents=img_data.read(),  # Read binary content of image
                        tag_ids=[tag.id]  # Assign the image to the corresponding tag
                    )

                    # Upload the image batch to Azure Custom Vision
                    upload_result = trainer.create_images_from_files(
                        project.id,
                        ImageFileCreateBatch(images=[entry])  # Wrap entry in a batch
                    )

                    # If upload failed, log error and raise exception
                    if not upload_result.is_batch_successful:
                        logger.error(f"Image upload failed for {image_file}. Reasons: {[e.message for e in upload_result.images]}")
                        raise CustomException(f"Upload failed for {image_file}")

                    logger.info("Image Upload Successful ({^,^})")
                except CustomException as e:
                    logger.error(e)
                    logger.error("Image Upload Failed ({-,-})")
                    raise CustomException(e)  # Propagate exception to main try block
except CustomException as e:
    logger.info("Exception occurred at ", e)
    logger.error(e)
    print(e)
    raise CustomException(e)  # Final exception raise if anything failed during upload


# Initiate model training
print(f"Initiating Training ..")
iteration = trainer.train_project(project.id)  # Start training on uploaded images
logger.info("Training Images initiated....")


# Polling loop: wait for training to complete by checking status every 5 seconds
print("Waiting for training to complete...")
count = 0
while iteration.status != "Completed":
    count += 1
    print(f"Training status: {iteration.status}, \niteration count:{count}")
    time.sleep(5)  # Wait 5 seconds before checking status again
    iteration = trainer.get_iteration(project.id, iteration.id)  # Refresh iteration status


# Set this trained iteration as the default version to use for predictions
try:
    logger.info("Training Images. \nProcessing !!!...")
    trainer.update_iteration(
        project.id,
        iteration.id,
        iteration.name,
        is_default=True  # Set this trained iteration as default
    )
    print(f"Training complete for {iteration.id}")
except CustomException as e:
    logger.error(e)
    raise CustomException(e)


# Publish the trained model so it can be used for predictions via the Prediction API
try:
    logger.info(f"Instantiating the model : {publish_iteration_name}")
    trainer.publish_iteration(
        project_id=project.id,
        iteration_id=iteration.id,
        publish_name=publish_iteration_name,  # Name to identify the published model
        prediction_id=resource_id_prediction  # Link to prediction endpoint resource
    )
    logger.info("Model published successfully ({-,-})")
except CustomException as e:
    logger.info("Model Failed to Publish ({-,-}) !!!")
    logger.error(e)
    raise CustomException(e)

print(f"Model published with name: {publish_iteration_name}")
# this project was done by Ashwin Ashok Pillai