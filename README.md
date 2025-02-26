Collecting workspace information# OutreachBot

OutreachBot is a full-stack application for file upload, processing, and generating personalized outreach content. The application consists of a React frontend for file management and a Python backend for data processing and AI-powered content generation.

## Getting Started

### 1. Cloning the Repository

```bash
# Clone the repository
git clone https://github.com/kevalshah14/OutreachBot

# Navigate to the project directory
cd OutreachBot
```

### 2. Setting Up the Frontend

The frontend is built with React and Vite, offering a modern UI for file upload and preview.

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173` (or the port specified by Vite).

#### Frontend Features

- Drag-and-drop file upload interface
- File preview for various formats (CSV, Excel, PDF, images)
- Responsive design with Tailwind CSS
- Smooth animations with Framer Motion

### 3. Setting Up the Backend

The backend is a Python FastAPI application that processes uploads and generates content.

```bash
# Navigate to the backend directory
cd backend

# Install Poetry if you don't have it
pip install poetry

# Install dependencies
poetry install

# Create .env file (see Environment Variables section below)
cp .env.example .env  # Then edit the .env file with your credentials

# Run the backend server
poetry run python -m app.main
```

The API will be available at `http://localhost:8000`.

#### Backend Features

- FastAPI for high-performance API endpoints
- File processing for various formats
- AI integration for content generation
- CSV data processing capabilities

### 4. Using test.py

The test.py script uses automated browser interaction to gather investment information from Perplexity AI.

```bash
# Navigate to the backend directory
cd backend

# Create an input CSV file if it doesn't exist
# Format: A header row with "company_name" and company names in rows below

# Run the script
poetry run python test.py
```

The script will:
1. Read company names from input.csv
2. Open a Chrome browser for each company
3. Query Perplexity AI for investment information
4. Save the results to output.csv

#### Requirements for test.py

- Google Chrome must be installed
- Internet connection required
- The process can take 5-10 minutes per company

### 5. Environment Variables (.env file)

Create a `.env` file in the backend directory with the following variables:

```
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration (for SendEmail.py)
GOOGLE_EMAIL=your_gmail_address
GOOGLE_EMAIL_PASSWORD=your_app_password

# FastAPI Configuration (optional)
UVICORN_HOST=127.0.0.1
UVICORN_PORT=8000
UVICORN_RELOAD=True

# Base URL (if using a custom API endpoint)
BASE_URL=https://api.example.com/v1
```

## Project Structure

```
.
├── backend/               # Python FastAPI backend
│   ├── app/               # Backend application code
│   │   ├── api/           # API routes
│   │   ├── models/        # Data models
│   │   ├── services/      # Business logic
│   │   └── main.py        # Application entry point
│   ├── GenerateEmail.py   # Email generation script
│   ├── sendEmail.py       # Email sending script
│   ├── test.py            # Investment data collection script
│   └── pyproject.toml     # Python dependencies
└── frontend/              # React frontend
    ├── public/            # Static assets
    ├── src/               # React components and logic
    │   ├── App.jsx        # Main application component
    │   ├── FileInputPage.jsx  # File upload interface
    │   ├── FileRenderPage.jsx # File preview interface
    │   └── assets/        # Frontend assets
    ├── package.json       # Node.js dependencies
    └── vite.config.js     # Vite configuration
```

## Technologies Used

- **Frontend**: React, Vite, Tailwind CSS, Framer Motion, XLSX
- **Backend**: FastAPI, Poetry, Pandas, Google Gemini AI, Selenium
- **Tools**: Undetected ChromeDriver, OpenAI API

## License

This project is proprietary and not licensed for redistribution or reuse without permission.