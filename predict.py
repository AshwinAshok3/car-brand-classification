# Import necessary libraries for prediction
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os
from logger import logger
from exception import CustomException

# Credentials and endpoints - update these with your own values
prediction_key = "4EEgJnAYXK1YEoul9UwV2ZoKILN9j3E9FM70D6RrPmcqWbuMuqwkJQQJ99BEACGhslBXJ3w3AAAIACOGFTs7"  # API key for prediction
prediction_endpoint = "https://automobileprediction.cognitiveservices.azure.com/"  # Your prediction endpoint URL
project_id = "c7bcc931-8118-4e40-9d39-89bf45f049d0"  # Your Custom Vision project ID
published_name = "car_brand_model_v1"  # Your published iteration name
project_name = "carBrandtraining"


# Authenticate the prediction client
credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)


# Function to predict a single image
def predict_single_image(image_path):
    with open(image_path, "rb") as image_data:
        results = predictor.classify_image(project_id, published_name, image_data.read())

    print(f"Predictions for image: {os.path.basename(image_path)}")
    for prediction in results.predictions:
        print(f"\t{prediction.tag_name}: {prediction.probability * 100:.2f}%")

# Function to batch predict all images in a folder
def predict_images_from_folder(folder_path):
    for image_file in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_file)
        if os.path.isfile(image_path):
            predict_single_image(image_path)
            print("-" * 40)

if __name__ == "__main__":
    # Example usage for a single image
    image_path = "test_images/car1.jpg"  # Change to your image path
    predict_single_image(image_path)

    # Example usage for batch prediction
    # folder_path = "test_images"
    # predict_images_from_folder(folder_path)
