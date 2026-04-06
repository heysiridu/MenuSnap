# 🍽️ MenuSnap (Under construction)

<div align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" />
</div>

<div align="center">
  <h3>Transform restaurant menus into interactive digital experiences using AI-powered OCR</h3>
  <p>Upload a photo → Extract text → Translate → Visualize with images</p>
</div>

---

## 📸 Demo

<div align="center">
  <p><i>Upload a menu photo and watch it transform into an interactive digital menu</i></p>
  <img width="3953" height="2342" alt="Image" src="https://github.com/user-attachments/assets/76d5ccab-8202-4d4b-9f60-bfd414544b41" />
  <p><i>figma link: https://www.figma.com/design/SvVpIbtYdMh2E2ZLHG3aQ2/MenuSnap-UI?node-id=77-83&t=EfY6s0pbsfePoF2w-1</i></p>
</div>

## ✨ Features

- 📷 **Smart Upload**: Drag-and-drop or capture menu photos directly
- 🔍 **OCR Processing**: Advanced text extraction using Google Vision API
- 🌐 **Multi-language Support**: Automatic language detection and translation
- 🖼️ **Visual Enhancement**: Automatic food images for each menu item
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile
- ⚡ **Real-time Processing**: Fast and efficient menu digitization
- 💾 **Export Options**: Save menus as JSON, PDF, or shareable links

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   React     │────▶│   FastAPI    │────▶│  Google Cloud   │
│  Frontend   │◀────│   Backend    │◀────│   Vision API    │
└─────────────┘     └──────────────┘     └─────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   Database   │
                    │  (Optional)  │
                    └──────────────┘
```

## 🚀 Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS / Material-UI
- **State Management**: React Hooks & Context API
- **HTTP Client**: Axios
- **Build Tool**: Create React App

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **OCR Engine**: Google Cloud Vision API
- **Image Processing**: OpenCV, Pillow
- **Translation**: Google Cloud Translation API
- **Server**: Uvicorn (ASGI)
- **Validation**: Pydantic

### Infrastructure
- **Container**: Docker
- **Database**: PostgreSQL / SQLite (optional)
- **File Storage**: Local / Google Cloud Storage
- **Deployment**: Heroku / Google Cloud Run / AWS

## 📋 Prerequisites

Before you begin, ensure you have:

- **Node.js** (v16 or higher)
- **Python** (3.9 or higher)
- **npm** or **yarn**
- **Git**
- **Google Cloud Account** with billing enabled
- **Google Cloud CLI** (optional)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MenuSnap.git
cd MenuSnap
```

### 2. Set Up Google Cloud

#### Enable Required APIs:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable the following APIs:
   - Cloud Vision API
   - Cloud Translation API

#### Create Service Account:
```bash
# Using gcloud CLI
gcloud iam service-accounts create menusnap-service \
    --display-name="MenuSnap Service Account"

# Download credentials
gcloud iam service-accounts keys create \
    ./backend/credentials/service-account.json \
    --iam-account=menusnap-service@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

#### Environment Variables (.env):
```env
# Server Configuration
PORT=8000
HOST=0.0.0.0
DEBUG=True

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=./credentials/service-account.json
GOOGLE_CLOUD_PROJECT=your-project-id

# CORS
FRONTEND_URL=http://localhost:3000

# Optional: Database
DATABASE_URL=sqlite:///./menusnap.db

# Optional: Secret Key
SECRET_KEY=your-secret-key-here
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
# or
yarn install

# Set up environment variables
cp .env.example .env.local
```

#### Environment Variables (.env.local):
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_MAPS_API_KEY=your-api-key (optional)
```

## 🎯 Usage

### Running Development Servers

#### Start Backend:
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the run script:
./run.sh
```

Backend will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Start Frontend:
```bash
cd frontend
npm start
# or
yarn start
```

Frontend will be available at: http://localhost:3000

### Running Both Servers Simultaneously:

#### Option 1: Using Make (if you have Makefile):
```bash
make run-all
```

#### Option 2: Using npm scripts (from root):
```bash
npm run dev
```

#### Option 3: Using two terminals:
```bash
# Terminal 1
cd backend && ./run.sh

# Terminal 2
cd frontend && npm start
```

## 📖 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/upload` | Upload menu image |
| POST | `/api/ocr` | Process image with OCR |
| POST | `/api/translate` | Translate menu items |
| GET | `/api/menu/{id}` | Get processed menu |
| POST | `/api/process` | Complete pipeline |

### Example API Call:

```python
import requests

# Upload image
with open('menu.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload',
        files={'file': f}
    )
    print(response.json())
```

### Response Format:
```json
{
  "success": true,
  "data": {
    "menu_items": [
      {
        "name": "Spaghetti Carbonara",
        "translated_name": "意大利培根蛋面",
        "price": 12.99,
        "image_url": "https://...",
        "confidence": 0.95
      }
    ],
    "original_text": "...",
    "language": "en",
    "processing_time": 2.34
  }
}
```

## 🧪 Testing

### Backend Tests:
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests:
```bash
cd frontend
npm test
```

### End-to-End Tests:
```bash
npm run test:e2e
```

## 📦 Project Structure

```
MenuSnap/
├── frontend/                 # React Frontend
│   ├── public/              # Static files
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Upload/     # Upload component
│   │   │   ├── MenuDisplay/ # Display component
│   │   │   └── common/     # Shared components
│   │   ├── services/       # API services
│   │   ├── hooks/          # Custom hooks
│   │   ├── utils/          # Helper functions
│   │   ├── types/          # TypeScript types
│   │   ├── App.tsx         # Main app component
│   │   └── index.tsx       # Entry point
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                  # Python Backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   └── routes/     # Route handlers
│   │   ├── core/           # Core configuration
│   │   ├── services/       # Business logic
│   │   │   ├── ocr_service.py
│   │   │   ├── translation_service.py
│   │   │   └── image_service.py
│   │   ├── models/         # Data models
│   │   ├── utils/          # Utilities
│   │   └── main.py         # FastAPI app
│   ├── tests/              # Test files
│   ├── uploads/            # Uploaded files
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
│
├── docs/                    # Documentation
├── docker-compose.yml      # Docker configuration
├── Makefile               # Build automation
├── .gitignore
└── README.md
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build separately
docker build -t menusnap-frontend ./frontend
docker build -t menusnap-backend ./backend
```

### Heroku Deployment

```bash
# Install Heroku CLI
# Create Heroku app
heroku create menusnap-api

# Deploy backend
git subtree push --prefix backend heroku main

# Set environment variables
heroku config:set GOOGLE_APPLICATION_CREDENTIALS=...
```

### Google Cloud Run

```bash
# Build and deploy backend
gcloud builds submit --tag gcr.io/PROJECT-ID/menusnap-backend ./backend
gcloud run deploy --image gcr.io/PROJECT-ID/menusnap-backend --platform managed
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Code refactoring
- `test:` Testing
- `chore:` Maintenance

## 🐛 Troubleshooting

### Common Issues

#### 1. Google Cloud Authentication Error
```bash
# Make sure credentials file exists and path is correct
export GOOGLE_APPLICATION_CREDENTIALS="./credentials/service-account.json"
```

#### 2. CORS Error
```python
# Check backend CORS settings match frontend URL
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Must match frontend URL
)
```

#### 3. Port Already in Use
```bash
# Find and kill process using the port
lsof -i :8000  # Find process
kill -9 <PID>  # Kill process
```


## 🙏 Acknowledgments

- Google Cloud Vision API for OCR capabilities
- FastAPI for the amazing Python framework
- React team for the excellent frontend framework
- All contributors and testers

## 📞 Support

For support, email support@menusnap.com or open an issue on GitHub.

## 🗺️ Roadmap

- [x] Basic OCR functionality
- [x] Multi-language support
- [ ] User authentication
- [ ] Menu history/saving
- [ ] Restaurant dashboard
- [ ] Mobile app
- [ ] AI-powered menu recommendations
- [ ] Nutritional information
- [ ] Allergen detection
- [ ] Price comparison

---

<div align="center">
  Made with ❤️ by the MenuSnap Team
</div>
