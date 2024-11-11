# NOTE: commenting out this file (for now), as we are using the Django ORM instead (can bring this back if needed)
# NOTE: bringing this back since it is needed to access supabase's storage system

from django.conf import settings
from supabase import create_client, Client
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

def get_supabase_client() -> Client:
  url: str = settings.SUPABASE_URL
  key: str = settings.SUPABASE_ANON_KEY
  return create_client(url, key)

# Load toxicity model
# Load tokenizer and model
model_name = "unitary/toxic-bert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

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
  inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

  # Get the model's predictions
  with torch.no_grad():
    outputs = model(**inputs)
  
  # Get the probability of toxic content (lower the more toxic)
  logits = outputs.logits
  probabilities = torch.softmax(logits, dim=1)
  toxicity_score = probabilities[0][1].item()

  # Return True if the toxicity score exceeds the threshold
  return toxicity_score <= threshold
