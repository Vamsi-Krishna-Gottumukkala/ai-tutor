# AI Personal Tutor

An AI-powered adaptive learning platform built with Django. This application provides personalized tutoring using Gemini vision/API for diagnostic analysis, course generation, and intelligent interactions. It also includes Google OAuth authentication for seamless sign-in.

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:
- **Python 3.8+** (We recommend Python 3.10+)
- **Git**
- A **PostgreSQL** database (Local or Cloud like Supabase/Neon)
- **Google Cloud Console Account** (for Google OAuth credentials)
- **Google Gemini API Key**

## Getting Started

Follow these step-by-step instructions to get a local copy up and running.

### 1. Clone the Repository

```bash
git clone https://github.com/Vamsi-Krishna-Gottumukkala/ai-tutor.git
cd ai-tutor
```

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

**For Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**For macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

*(Optional)* Since this project uses Natural Language Processing libraries like `spacy` and possibly `NLTK`, you might need to download the language models to prevent any `ModuleNotFoundError`:

```bash
python -m spacy download en_core_web_sm
# If you run into NLTK errors at runtime, you can also run:
# python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

### 4. Setup Environment Variables

The project uses `.env` files to manage secrets and API keys safely without committing them to the repository.

Create a file named `.env` in the root directory (the same folder as `manage.py`) and add the following configuration, replacing the placeholder values with your actual credentials:

```env
# Security Warning: Keep your secret key secret in production!
SECRET_KEY=your_secure_random_secret_key_here
DEBUG=True

# Database Configuration
# Update these with your PostgreSQL server details (e.g., Supabase)
DB_NAME=postgres
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host_url
DB_PORT=5432

# External API Keys and Integrations
GEMINI_API_KEY=your_gemini_api_key_here

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

### 5. Setup the Database

Apply the database migrations to set up the necessary schemas for Django, AllAuth, and the application's models:

```bash
python manage.py makemigrations
python manage.py migrate
```

*(Optional)* You can also create a superuser to access the Django admin panel:

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

Finally, start the local server:

```bash
python manage.py runserver
```

You can now access the application by opening your web browser and navigating to:
**http://127.0.0.1:8000/**

## Accessing Admin Panel
Log into `http://127.0.0.1:8000/admin` using the superuser account created in step 5 to tweak databases, verify social connection settings, or manage existing records.

## Troubleshooting

- **Google Login fails/SocialApp matching query does not exist:** Ensure you have configured the `Social Application` correctly in the Django Admin panel for the `google` provider with your Client ID and Client Secret, and assigned the `example.com` or `localhost` site to it.
- ** psycopg2 installation errors:** On Windows, you may need to install PostgreSQL and add the `pg_config` path. Using `psycopg2-binary` (which is already in `requirements.txt`) usually resolves this without extra compiler tools.
