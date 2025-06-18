from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import assemblyai as aai
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import uuid
import logging
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure API keys
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not aai.settings.api_key:
    logger.error("AssemblyAI API key not found in environment variables")
    raise ValueError("AssemblyAI API key not found in environment variables")

# Initialize OpenAI client
client = OpenAI(
    base_url="https://litellm.rillavoice.com/v1",
    api_key="sk-rilla-vibes"
)

# In-memory storage for stories (replace with a database in production)
stories = []

class Story(BaseModel):
    id: str
    text: str
    enhanced_text: str
    created_at: str
    reactions: Dict[str, int]

class StoryReaction(BaseModel):
    reaction_type: str

def enhance_text_with_llm(text: str) -> str:
    try:
        prompt = f"""Please enhance the following story while maintaining its core message and emotional impact. 
        Make it more engaging and well-written, but keep the original meaning intact:

        {text}"""

        response = client.chat.completions.create(
            model="claude-3-5-haiku",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
            
    except Exception as e:
        logger.error(f"Error in LLM processing: {str(e)}")
        raise HTTPException(status_code=500, detail="Error enhancing story with LLM")

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        logger.info(f"Received audio file: {file.filename}")
        
        # Create a temporary file with proper extension
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
        temp_file_path = temp_file.name
        
        try:
            # Write the uploaded file to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file.close()
            
            logger.info(f"Saved temporary file at: {temp_file_path}")
            
            # Transcribe using AssemblyAI
            config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
            logger.info("Starting transcription with AssemblyAI")
            
            transcript = aai.Transcriber(config=config).transcribe(temp_file_path)
            
            if transcript.status == "error":
                error_msg = f"Transcription failed: {transcript.error}"
                logger.error(error_msg)
                raise HTTPException(status_code=400, detail=error_msg)
            
            logger.info("Transcription completed successfully")
            return {"text": transcript.text}
            
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
                logger.info("Temporary file cleaned up")
            except Exception as e:
                logger.warning(f"Error cleaning up temporary file: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error processing audio upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/enhance-story")
async def enhance_story(story: Story):
    try:
        logger.info("Enhancing story with LLM")
        
        # Use the LLM to enhance the story
        enhanced_text = enhance_text_with_llm(story.text)
        logger.info("Story enhancement completed")

        # Create new story with enhanced text
        new_story = Story(
            id=str(uuid.uuid4()),
            text=story.text,
            enhanced_text=enhanced_text,
            created_at=datetime.now().isoformat(),
            reactions={"funny": 0, "happy": 0, "emotional": 0}
        )

        # Store the story
        stories.append(new_story)

        return new_story
    except Exception as e:
        logger.error(f"Error enhancing story: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stories")
async def get_stories():
    return stories

@app.post("/stories/{story_id}/react")
async def react_to_story(story_id: str, reaction: StoryReaction):
    # Find the story
    story = next((s for s in stories if s.id == story_id), None)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Update the reaction count
    if reaction.reaction_type in story.reactions:
        story.reactions[reaction.reaction_type] += 1
        return story
    else:
        raise HTTPException(status_code=400, detail="Invalid reaction type")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 