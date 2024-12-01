from django.conf import settings
from supabase import create_client, Client
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    AutoProcessor,
    FocalNetForImageClassification,
)
from torchvision import transforms
from PIL import Image
from io import BytesIO
import torch


def get_supabase_client() -> Client:
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_ANON_KEY
    return create_client(url, key)


def create_bucket_if_not_exists(bucket_name):
    """
    Checks if the specified bucket exists and creates it if it doesn't.
    """
    supabase = get_supabase_client()

    # Check if the bucket exists
    buckets = supabase.storage.list_buckets()

    # Check if the response is successful and get the list of buckets
    if isinstance(buckets, list):

        # Get all bucket names
        bucket_names = [bucket.name for bucket in buckets]

        # Check if the specified bucket already exists
        if bucket_name in bucket_names:
            print(f"Bucket '{bucket_name}' already exists.")
        else:
            # Create the bucket since it doesn't exist
            try:
                response = supabase.storage.create_bucket(bucket_name)
                if "error" in response:
                    print(f"Error creating bucket: {response['error']}")
                    return False
                else:
                    print(f"Bucket '{bucket_name}' created successfully.")
                return True
            except Exception as e:
                print("Error creating bucket: ", e)
                return False
    else:
        print(f"Unexpected response format: {buckets}")

    return True


# Ensure the code runs on CPU only
device = torch.device("cpu")

# Load toxicity model
# Load tokenizer and model
text_model_name = "unitary/toxic-bert"
tokenizer = AutoTokenizer.from_pretrained(text_model_name)
model = AutoModelForSequenceClassification.from_pretrained(text_model_name)
model.to(device)

# Load image toxicity model
# img_model_name = "MichalMlodawski/nsfw-image-detection-large"
# processor = AutoProcessor.from_pretrained(img_model_name)
# model_img = FocalNetForImageClassification.from_pretrained(img_model_name)
# model_img.eval()

# Image transformations
transform = transforms.Compose(
    [
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# Mapping from model labels to NSFW categories
label_to_category = {"LABEL_0": "Safe", "LABEL_1": "Questionable", "LABEL_2": "Unsafe"}


def check_content(text, threshold=0.003):
    """
    Checks if the provided text contains toxic content.

    Args:
      text (str): The message to check for toxicity.
      threshold (float): Minimum confidence level for detecting toxicity.

    Returns:
      bool: True if toxic content is detected, otherwise False.
    """

    # Encode the input text
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, padding=True, max_length=512
    )

    # Get the model's predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the probability of toxic content (lower the more toxic)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    toxicity_score = probabilities[0][1].item()

    # Return True if the toxicity score exceeds the threshold
    return toxicity_score <= threshold
