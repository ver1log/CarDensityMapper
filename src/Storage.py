from supabase import create_client
import pandas as pd
from dotenv import load_dotenv
import os
import json
import io
import requests  # Needed for fetching files from public URLs

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Base URL for public storage
PUBLIC_STORAGE_URL = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}"

# Function to fetch CSV file from public URL
def fetch_csv_from_supabase(file_path):
    public_url = f"{PUBLIC_STORAGE_URL}/{file_path}"
    response = requests.get(public_url)
    return pd.read_csv(io.StringIO(response.text))

# Function to fetch JSON file from public URL
def fetch_json_from_supabase(file_path):
    public_url = f"{PUBLIC_STORAGE_URL}/{file_path}"
    response = requests.get(public_url)
    return json.loads(response.text)
