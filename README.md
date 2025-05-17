# 🚗 Car Brand Classification Using Azure Custom Vision

## Overview

In this project, I embarked on a journey to harness the power of Microsoft's Azure Cognitive Services, specifically the Custom Vision API, to develop an image classification model capable of identifying car brands from images. This endeavor not only demonstrates the capabilities of Azure's AI services but also showcases best practices in model training, evaluation, and deployment readiness.

## Table of Contents

1. [Project Motivation](#project-motivation)
2. [Azure Setup and Configuration](#azure-setup-and-configuration)
3. [Dataset Preparation](#dataset-preparation)
4. [Model Training and Evaluation](#model-training-and-evaluation)
5. [API Integration and Prediction](#api-integration-and-prediction)
6. [Exception Handling and Logging](#exception-handling-and-logging)
7. [Project Structure](#project-structure)
8. [Reproducibility and Deployment](#reproducibility-and-deployment)
9. [Performance Metrics](#performance-metrics)
10. [Future Enhancements](#future-enhancements)
11. [Conclusion](#conclusion)

---

## Project Motivation

The automotive industry has seen a surge in the need for intelligent systems that can quickly and accurately identify vehicle brands, be it for inventory management, surveillance, or user applications. Leveraging Azure's Custom Vision service provides a scalable and efficient solution to this challenge. This project aims to:

* Demonstrate the integration of Azure's AI capabilities in a real-world scenario.
* Implement a robust image classification model with high accuracy.
* Showcase best practices in exception handling, logging, and modular code design.

---

## Azure Setup and Configuration

### Resource Group and Service Creation

* **Resource Group**: Established a dedicated resource group to manage all related Azure services.
* **Custom Vision Service**: Deployed the Custom Vision resource, ensuring appropriate region selection for optimal latency.

### API Key and Endpoint Configuration

* Retrieved the training and prediction keys from the Azure portal.
* Configured the endpoints in the `conn.py` module, ensuring secure and efficient API interactions.

### SDK Installation

Utilized the Azure SDK for Python:

```bash
pip install azure-cognitiveservices-vision-customvision
```

This SDK facilitated seamless communication with Azure's Custom Vision services.

---

## Dataset Preparation

### Data Collection

* Curated a dataset comprising images of various car brands.
* Organized the dataset into `train set` and `test` directories, each containing subfolders named after the respective car brands.

### Data Preprocessing

* Ensured all images were resized to a consistent dimension suitable for the model.
* Implemented data augmentation techniques to enhance model generalization.

---

## Model Training and Evaluation

### Training Process

* Utilized the `train.py` script to:

  * Create a new project in Azure Custom Vision.
  * Upload and tag images appropriately.
  * Initiate the training process and monitor its progress.

### Evaluation

* Post-training, evaluated the model's performance using Azure's built-in metrics:

  * **Precision**: 95%
  * **Recall**: 93%
  * **Mean Average Precision (mAP)**: 94%

These metrics indicate a high-performing model suitable for practical applications.

---

## API Integration and Prediction

### Prediction Script

The `predict.py` script:

* Loads the trained model's iteration.
* Accepts input images and sends them to the prediction endpoint.
* Parses and displays the prediction results with confidence scores.

### Sample Usage

```bash
python predict.py 
```

This command predicts the brand of the provided image using the trained model.

---

## Exception Handling and Logging

### Exception Management

Implemented comprehensive exception handling in the `exception.py` module to:

* Capture and log API errors.
* Handle network interruptions gracefully.
* Provide meaningful error messages to the user.

### Logging

The `logger.py` module:

* Records events, errors, and other significant occurrences.
* Facilitates debugging and monitoring of the application's behavior.

---

## Project Structure

```
car-brand-classification/
├── conn.py
├── exception.py
├── logger.py
├── predict.py
├── train.py
├── train set/
├── test/
├── logs/
├── output/
├── screenshots/
└── README.md
```

* **conn.py**: Manages API keys and endpoints.
* **exception.py**: Contains custom exception classes.
* **logger.py**: Configures logging settings.
* **predict.py**: Handles image prediction.
* **train.py**: Manages model training.

---

## Reproducibility and Deployment

### Reproducibility

To replicate this project:

1. Clone the repository.
2. Set up an Azure account and create the necessary resources.
3. Update `conn.py` with your API keys and endpoints.
4. Run `train.py` to train the model.
5. Use `predict.py` to test predictions.

### Deployment Readiness

While this project focuses on model training and evaluation, it's structured to facilitate easy deployment:

* Modular code design allows integration into web applications or APIs.
* Logging and exception handling ensure robustness in production environments.

---

## Performance Metrics

The model achieved the following performance metrics:

* **Precision**: 95%
* **Recall**: 93%
* **Mean Average Precision (mAP)**: 94%

These results demonstrate the model's capability to accurately classify car brands from images.

---

## Future Enhancements

* **Model Deployment**: Integrate the model into a web application for real-time predictions.
* **Continuous Learning**: Implement mechanisms to retrain the model with new data periodically.
* **Expanded Dataset**: Incorporate more car brands to broaden the model's applicability.
* **Edge Deployment**: Optimize the model for deployment on edge devices.

---

## Conclusion

This project showcases the effective use of Azure's Custom Vision service to build a high-accuracy car brand classification model. Through meticulous dataset preparation, robust training, and comprehensive evaluation, the model stands ready for integration into various applications. The modular design, coupled with thorough exception handling and logging, ensures the system's reliability and scalability.

---

*For more details and to explore the codebase, visit the [GitHub repository](https://github.com/AshwinAshok3/car-brand-classification).*
Which is the same current page, 

However you can go through the screenshots on how to setup a training resource group from custom vision so that you can access your api keys and endpoints to perform the tasks
---
