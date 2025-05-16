# importing libraries
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials
import os
from logger import logger
from exception import CustomException
import time

# giving api keys to training set
endpoint = "https://automobiletraining.cognitiveservices.azure.com/"
api_key1 = "FLaCIQL2b83tQjKSqmOsYpTl3pIFQUffh7ciVNIvuPUKQ35gII6MJQQJ99BEACGhslBXJ3w3AAAJACOGuNew"
project_name = "carBrandtraining"

# Authenticating
try:
    logger.info("Authenticating API - ENDPOINT")
    credentials = ApiKeyCredentials(in_headers= {"Training-key":api_key1})
    trainer = CustomVisionTrainingClient(endpoint, credentials)
except Exception as e:
    logger.error(e)
    raise CustomException(e)

# Creating the project
logger.info("Initializing Project Name")
project = trainer.create_project(project_name)
logger.info("Project Name created successfully")

# providing dataset path and tags for each car brand
database = "train set"
logger.info("Database Initiated")

# printing items for grandmarquis mercury
for imgdir in os.listdir(database):
    print(imgdir)


# making or creating tags for my models
for label in os.listdir(database):
    tag = trainer.create_tag(project.id, label)
    label_path = os.path.join(database, label)

    for image_name in os.listdir(label_path):
        with open(os.path.join(label_path, image_name), "rb") as img_data:
            try:
                logger.info(f"Uploading  {image_name}....given tag {tag.name}....path {label_path}")
                trainer.create_images_from_data(project.id, img_data.read(), tag_ids=[tag.id])
                logger.info("Image Upload Successful ({^,^})")
            except CustomException as e:
                logger.error(e)
                logger.error("Image Upload Failed ({-,-})")
                raise CustomException(e)
        # print(f"Image Name : {image_name}, tag name : {tag.name}, path label : {label_path}")

# Train the model on Custom Vision
print(f"Initiating Training ..")
iteration = trainer.train_project(project.id)
logger.info("Training Images initiation")

# Wait until training is completed
print("Waiting for training to complete...")
while True:
    current_iteration = trainer.get_iteration(project.id, iteration.id)
    status = current_iteration.status
    print(f"Current Status: {status}")

    if status == "Completed":
        break
    elif status in ["Failed", "Canceled"]:
        raise CustomException(f"Training {status}. Please check the logs or dataset.")

    time.sleep(5)

# Set the trained iteration as default
try:
    logger.info("Training Images. \nProcessing !!!...")
    trainer.update_iteration(project.id,
                             iteration.id,
                             current_iteration.name,
                             is_default=True)
    print(f"✅ Training complete for {iteration.id}")
except CustomException as e:
    logger.error(e)
    raise CustomException(e)
