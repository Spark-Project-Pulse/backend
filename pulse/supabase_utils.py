# NOTE: commenting out this file (for now), as we are using the Django ORM instead (can bring this back if needed)
# NOTE: bringing this back since it is needed to access supabase's storage system

from django.conf import settings
from supabase import create_client, Client

def get_supabase_client() -> Client:
  url: str = settings.SUPABASE_URL
  key: str = settings.SUPABASE_ANON_KEY
  return create_client(url, key)

from transformers import pipeline

# Load toxicity model
toxicity_model = pipeline("text-classification", model="unitary/toxic-bert", return_all_scores=True)

def checkContent(text, threshold=0.9):
  """
  Checks if the provided text contains toxic content.

  Args:
    text (str): The message to check for toxicity.
    threshold (float): Minimum confidence level for detecting toxicity.

  Returns:
    bool: True if toxic content is detected, otherwise False.
  """

  # Run the model on the input text
  predictions = toxicity_model(text)

  # Process the model's output
  for prediction in predictions[0]:
    # Check if label is 'toxic' and confidence is above threshold
    if prediction['label'] == 'toxic' and prediction['score'] >= threshold:
      print('Toxicity found')
      return True

  print('No toxicity found')
  return False
