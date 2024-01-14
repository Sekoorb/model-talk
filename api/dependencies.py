from .config import settings
from supabase import create_client, Client

# Initialize Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

# Other dependencies like JWT token validation can be added here
