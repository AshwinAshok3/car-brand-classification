# importing libraries for custom vision Prediction
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os
import shutil
from logger import logger
from exception import CustomException
logger.info("Imported Libraries")


# Credentials and project details
prediction_key = "4EEgJnAYXK1YEoul9UwV2ZoKILN9j3E9FM70D6RrPmcqWbuMuqwkJQQJ99BEACGhslBXJ3w3AAAIACOGFTs7"
prediction_endpoint = "https://automobileprediction.cognitiveservices.azure.com/"
project_id = "c7bcc931-8118-4e40-9d39-89bf45f049d0"
published_name = "car_brand_model_v1"
logger.info("Credentials Saved")

# Paths for the test images and for the output dir making a new one
input_folder = "test"
output_folder = "output"
logger.info("Folder path specified for test data")


# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)
logger.info("Created an empty folder 'output' !")

# Authenticate prediction client
try:
    logger.info("Authentication for Credentials Successfull  ({^.^}) /")
    credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)
except Exception as e:
    logger.error(e)
    logger.info("Credential Authentication Failed ({-,-})")
    raise CustomException(e)



# Batch process folder
def predict_folder(folder_path):
    for file in os.listdir(folder_path):
        logger.info("Folder Path Verified")
        img_path = os.path.join(folder_path, file)
        if os.path.isfile(img_path):
            logger.info(f"Image File Verified {file}")
            predict_and_save(img_path)


# Predict and copy with renamed output
def predict_and_save(image_path):
    try :
        logger.info("Reading the Image file ")
        with open(image_path, "rb") as image_data:
            results = predictor.classify_image(project_id, published_name, image_data.read())
    except Exception as e:
        logger.error(e)

    logger.info("Prep for the prediction")
    # Get top prediction
    top_prediction = max(results.predictions, key=lambda x: x.probability)
    predicted_label = top_prediction.tag_name
    confidence = top_prediction.probability * 100

    # Print to console
    print(f"Predicted: {predicted_label} ({confidence:.2f}%) - {os.path.basename(image_path)}")

    # Create new filename and copy to output folder
    original_name = os.path.basename(image_path)
    name, ext = os.path.splitext(original_name)
    new_filename = f"{name}__predictedAS__{predicted_label}{ext}"
    new_path = os.path.join(output_folder, new_filename)

    shutil.copy(image_path, new_path)

if __name__ == "__main__":
    predict_folder(input_folder)
