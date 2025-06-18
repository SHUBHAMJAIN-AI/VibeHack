# Story Memory App

A web application that allows users to record voice messages, transcribe them into text, enhance the stories using Rilla Voice LLM (Claude), and share them with emotional reactions.

## Features

- Voice recording and transcription using AssemblyAI
- Story enhancement using Rilla Voice LLM (Claude)
- Emotional reactions (funny, happy, emotional)
- Modern Material-UI interface
- Real-time story updates

## Prerequisites

- Python 3.8+
- Node.js 14+
- AssemblyAI API key

## Setup

1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory with your API keys:
   ```
   ASSEMBLYAI_API_KEY=your_assemblyai_api_key
   ```

4. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000`

## Usage

1. Click the "Start Recording" button to begin recording your voice message
2. Click "Stop Recording" when you're done
3. Wait for the transcription and enhancement process to complete
4. View your story and add emotional reactions
5. Share your story with others

## Technologies Used

- Backend:
  - FastAPI
  - AssemblyAI
  - Rilla Voice LLM (Claude)
  - Python

- Frontend:
  - React
  - Material-UI
  - Axios
  - Web Audio API 