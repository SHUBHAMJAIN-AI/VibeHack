# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Dict, Optional
# import assemblyai as aai
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# import json
# from datetime import datetime
# import uuid
# import logging
# import tempfile

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# load_dotenv()

# app = FastAPI()

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Configure API keys
# aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
# if not aai.settings.api_key:
#     logger.error("AssemblyAI API key not found in environment variables")
#     raise ValueError("AssemblyAI API key not found in environment variables")

# # Initialize OpenAI client
# client = OpenAI(
#     base_url="https://litellm.rillavoice.com/v1",
#     api_key="sk-rilla-vibes"
# )

# # In-memory storage for stories (replace with a database in production)
# stories = []

# class Story(BaseModel):
#     id: str
#     text: str
#     enhanced_text: str
#     created_at: str
#     reactions: Dict[str, int]

# class StoryReaction(BaseModel):
#     reaction_type: str

# def enhance_text_with_llm(text: str) -> str:
#     try:
#         prompt = f"""Please enhance the following story while maintaining its core message and emotional impact. 
#         Make it more engaging and well-written, but keep the original meaning intact:

#         {text}"""

#         response = client.chat.completions.create(
#             model="claude-3-5-haiku",
#             messages=[{"role": "user", "content": prompt}]
#         )
        
#         return response.choices[0].message.content
            
#     except Exception as e:
#         logger.error(f"Error in LLM processing: {str(e)}")
#         raise HTTPException(status_code=500, detail="Error enhancing story with LLM")

# @app.post("/upload-audio")
# async def upload_audio(file: UploadFile = File(...)):
#     try:
#         logger.info(f"Received audio file: {file.filename}")
        
#         # Create a temporary file with proper extension
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
#         temp_file_path = temp_file.name
        
#         try:
#             # Write the uploaded file to the temporary file
#             content = await file.read()
#             temp_file.write(content)
#             temp_file.close()
            
#             logger.info(f"Saved temporary file at: {temp_file_path}")
            
#             # Transcribe using AssemblyAI
#             config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
#             logger.info("Starting transcription with AssemblyAI")
            
#             transcript = aai.Transcriber(config=config).transcribe(temp_file_path)
            
#             if transcript.status == "error":
#                 error_msg = f"Transcription failed: {transcript.error}"
#                 logger.error(error_msg)
#                 raise HTTPException(status_code=400, detail=error_msg)
            
#             logger.info("Transcription completed successfully")
#             return {"text": transcript.text}
            
#         except Exception as e:
#             logger.error(f"Error during transcription: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
            
#         finally:
#             # Clean up temporary file
#             try:
#                 os.unlink(temp_file_path)
#                 logger.info("Temporary file cleaned up")
#             except Exception as e:
#                 logger.warning(f"Error cleaning up temporary file: {str(e)}")
                
#     except Exception as e:
#         logger.error(f"Error processing audio upload: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/enhance-story")
# async def enhance_story(story: Story):
#     try:
#         logger.info("Enhancing story with LLM")
        
#         # Use the LLM to enhance the story
#         enhanced_text = enhance_text_with_llm(story.text)
#         logger.info("Story enhancement completed")

#         # Create new story with enhanced text
#         new_story = Story(
#             id=str(uuid.uuid4()),
#             text=story.text,
#             enhanced_text=enhanced_text,
#             created_at=datetime.now().isoformat(),
#             reactions={"funny": 0, "happy": 0, "emotional": 0}
#         )

#         # Store the story
#         stories.append(new_story)

#         return new_story
#     except Exception as e:
#         logger.error(f"Error enhancing story: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/stories")
# async def get_stories():
#     return stories

# @app.post("/stories/{story_id}/react")
# async def react_to_story(story_id: str, reaction: StoryReaction):
#     # Find the story
#     story = next((s for s in stories if s.id == story_id), None)
#     if not story:
#         raise HTTPException(status_code=404, detail="Story not found")

#     # Update the reaction count
#     if reaction.reaction_type in story.reactions:
#         story.reactions[reaction.reaction_type] += 1
#         return story
#     else:
#         raise HTTPException(status_code=400, detail="Invalid reaction type")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001) 
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Dict, Optional
# import assemblyai as aai
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# import json
# from datetime import datetime
# import uuid
# import logging
# import tempfile

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# load_dotenv()

# app = FastAPI(title="Story Memory API", version="1.0.0")

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Configure API keys
# aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
# if not aai.settings.api_key:
#     logger.error("AssemblyAI API key not found in environment variables")
#     raise ValueError("AssemblyAI API key not found in environment variables")

# # Initialize OpenAI client
# client = OpenAI(
#     base_url="https://litellm.rillavoice.com/v1",
#     api_key="sk-rilla-vibes"
# )

# # In-memory storage for stories (replace with a database in production)
# stories = []

# class Story(BaseModel):
#     id: str
#     text: str
#     enhanced_text: str
#     created_at: str
#     reactions: Dict[str, int]

# class StoryReaction(BaseModel):
#     reaction_type: str

# def enhance_text_with_llm(text: str) -> str:
#     """Enhance the story text using LLM while preserving the original meaning."""
#     try:
#         prompt = f"""Please enhance the following story while maintaining its core message and emotional impact. 
#         Make it more engaging and well-written, but keep the original meaning intact.
#         Focus on improving flow, adding vivid details, and enhancing emotional resonance.
        
#         Original story:
#         {text}
        
#         Enhanced version:"""

#         response = client.chat.completions.create(
#             model="claude-3-5-haiku",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=1000,
#             temperature=0.7
#         )
        
#         enhanced_text = response.choices[0].message.content
#         logger.info("Story enhancement completed successfully")
#         return enhanced_text
            
#     except Exception as e:
#         logger.error(f"Error in LLM processing: {str(e)}")
#         raise HTTPException(status_code=500, detail="Error enhancing story with LLM")

# @app.get("/")
# async def root():
#     """Health check endpoint."""
#     return {"message": "Story Memory API is running", "version": "1.0.0"}

# @app.post("/upload-audio")
# async def upload_audio(file: UploadFile = File(...)):
#     """Upload and transcribe audio file."""
#     try:
#         logger.info(f"Received audio file: {file.filename}, size: {file.size} bytes")
        
#         # Validate file type
#         if not file.content_type or not file.content_type.startswith('audio'):
#             logger.warning(f"Invalid file type: {file.content_type}")
#             raise HTTPException(status_code=400, detail="Please upload an audio file")
        
#         # Create a temporary file with proper extension
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
#         temp_file_path = temp_file.name
        
#         try:
#             # Write the uploaded file to the temporary file
#             content = await file.read()
#             if len(content) == 0:
#                 raise HTTPException(status_code=400, detail="Uploaded file is empty")
                
#             temp_file.write(content)
#             temp_file.close()
            
#             logger.info(f"Saved temporary file at: {temp_file_path}")
            
#             # Transcribe using AssemblyAI
#             config = aai.TranscriptionConfig(
#                 speech_model=aai.SpeechModel.best,
#                 language_detection=True,
#                 punctuate=True,
#                 format_text=True
#             )
#             logger.info("Starting transcription with AssemblyAI")
            
#             transcript = aai.Transcriber(config=config).transcribe(temp_file_path)
            
#             if transcript.status == "error":
#                 error_msg = f"Transcription failed: {transcript.error}"
#                 logger.error(error_msg)
#                 raise HTTPException(status_code=400, detail=error_msg)
            
#             if not transcript.text or len(transcript.text.strip()) == 0:
#                 raise HTTPException(status_code=400, detail="No speech detected in the audio file")
            
#             logger.info("Transcription completed successfully")
#             return {"text": transcript.text.strip()}
            
#         except HTTPException:
#             raise
#         except Exception as e:
#             logger.error(f"Error during transcription: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
            
#         finally:
#             # Clean up temporary file
#             try:
#                 os.unlink(temp_file_path)
#                 logger.info("Temporary file cleaned up")
#             except Exception as e:
#                 logger.warning(f"Error cleaning up temporary file: {str(e)}")
                
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error processing audio upload: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")

# @app.post("/enhance-story", response_model=Story)
# async def enhance_story(story: Story):
#     """Enhance a story using LLM and store it."""
#     try:
#         logger.info("Enhancing story with LLM")
        
#         if not story.text or len(story.text.strip()) == 0:
#             raise HTTPException(status_code=400, detail="Story text cannot be empty")
        
#         # Use the LLM to enhance the story
#         enhanced_text = enhance_text_with_llm(story.text)
        
#         # Create new story with enhanced text
#         new_story = Story(
#             id=str(uuid.uuid4()),
#             text=story.text.strip(),
#             enhanced_text=enhanced_text.strip(),
#             created_at=datetime.now().isoformat(),
#             reactions={"funny": 0, "happy": 0, "emotional": 0}
#         )

#         # Store the story
#         stories.append(new_story)
#         logger.info(f"Story stored with ID: {new_story.id}")

#         return new_story
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error enhancing story: {str(e)}")
#         raise HTTPException(status_code=500, detail="Error enhancing story")

# @app.get("/stories")
# async def get_stories():
#     """Get all stories."""
#     logger.info(f"Returning {len(stories)} stories")
#     return {"stories": stories, "count": len(stories)}

# @app.post("/stories/{story_id}/react", response_model=Story)
# async def react_to_story(story_id: str, reaction: StoryReaction):
#     """Add a reaction to a story."""
#     try:
#         # Find the story
#         story = next((s for s in stories if s.id == story_id), None)
#         if not story:
#             raise HTTPException(status_code=404, detail="Story not found")

#         # Validate reaction type
#         valid_reactions = ["funny", "happy", "emotional"]
#         if reaction.reaction_type not in valid_reactions:
#             raise HTTPException(
#                 status_code=400, 
#                 detail=f"Invalid reaction type. Must be one of: {', '.join(valid_reactions)}"
#             )

#         # Update the reaction count
#         story.reactions[reaction.reaction_type] += 1
#         logger.info(f"Added {reaction.reaction_type} reaction to story {story_id}")
        
#         return story
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error adding reaction: {str(e)}")
#         raise HTTPException(status_code=500, detail="Error adding reaction")

# @app.delete("/stories/{story_id}")
# async def delete_story(story_id: str):
#     """Delete a story."""
#     global stories
#     original_count = len(stories)
#     stories = [s for s in stories if s.id != story_id]
    
#     if len(stories) == original_count:
#         raise HTTPException(status_code=404, detail="Story not found")
    
#     logger.info(f"Deleted story {story_id}")
#     return {"message": "Story deleted successfully"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")

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

app = FastAPI(title="Story Memory API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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
    title: str
    category: str
    text: str
    enhanced_text: str
    created_at: str
    reactions: Dict[str, int]

class StoryReaction(BaseModel):
    reaction_type: str

def enhance_text_with_llm(text: str) -> dict:
    """Enhance the story text and classify its category."""
    try:
        prompt = f"""Please analyze this personal story and help make it more memorable and touching:

1. Enhance the story to be more vivid and emotionally engaging while keeping the authentic, conversational voice
2. Add sensory details, emotions, and small moments that make people smile or feel connected
3. Keep it warm and relatable - like a story a beloved grandparent would tell
4. Create a simple, memorable title (3-6 words)
5. Choose the main emotion: funny, happy, or emotional

Make it the kind of story people want to share and remember, not fancy writing.

Original story:
{text}

Please respond in this exact format:
TITLE: [simple, memorable title]
CATEGORY: [funny/happy/emotional]  
ENHANCED: [enhanced story with heart, warmth, and memorable details]"""

        response = client.chat.completions.create(
            model="claude-3-5-haiku",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        
        # Parse the response
        lines = result.split('\n')
        title = ""
        category = "happy"  # default
        enhanced_text = ""
        
        enhanced_started = False
        for line in lines:
            if line.startswith("TITLE:"):
                title = line.replace("TITLE:", "").strip()
            elif line.startswith("CATEGORY:"):
                category = line.replace("CATEGORY:", "").strip().lower()
                if category not in ["funny", "happy", "emotional"]:
                    category = "happy"
            elif line.startswith("ENHANCED:"):
                enhanced_text = line.replace("ENHANCED:", "").strip()
                enhanced_started = True
            elif enhanced_started and line.strip():
                enhanced_text += " " + line.strip()
        
        # Fallback if parsing fails
        if not enhanced_text:
            enhanced_text = result
        if not title:
            # Generate title from first few words
            words = text.split()[:4]
            title = " ".join(words) + ("..." if len(words) == 4 else "")
        
        logger.info("Story enhancement and classification completed successfully")
        return {
            "enhanced_text": enhanced_text,
            "title": title,
            "category": category
        }
            
    except Exception as e:
        logger.error(f"Error in LLM processing: {str(e)}")
        raise HTTPException(status_code=500, detail="Error enhancing story with LLM")

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Story Memory API is running", "version": "1.0.0"}

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """Upload and transcribe audio file."""
    try:
        logger.info(f"Received audio file: {file.filename}, size: {file.size} bytes")
        
        # Validate file type
        if not file.content_type or not file.content_type.startswith('audio'):
            logger.warning(f"Invalid file type: {file.content_type}")
            raise HTTPException(status_code=400, detail="Please upload an audio file")
        
        # Create a temporary file with proper extension
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
        temp_file_path = temp_file.name
        
        try:
            # Write the uploaded file to the temporary file
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
                
            temp_file.write(content)
            temp_file.close()
            
            logger.info(f"Saved temporary file at: {temp_file_path}")
            
            # Transcribe using AssemblyAI
            config = aai.TranscriptionConfig(
                speech_model=aai.SpeechModel.best,
                language_detection=True,
                punctuate=True,
                format_text=True
            )
            logger.info("Starting transcription with AssemblyAI")
            
            transcript = aai.Transcriber(config=config).transcribe(temp_file_path)
            
            if transcript.status == "error":
                error_msg = f"Transcription failed: {transcript.error}"
                logger.error(error_msg)
                raise HTTPException(status_code=400, detail=error_msg)
            
            if not transcript.text or len(transcript.text.strip()) == 0:
                raise HTTPException(status_code=400, detail="No speech detected in the audio file")
            
            logger.info("Transcription completed successfully")
            return {"text": transcript.text.strip()}
            
        except HTTPException:
            raise
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
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing audio upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/enhance-story", response_model=Story)
async def enhance_story(story: Story):
    """Enhance a story using LLM and store it."""
    try:
        logger.info("Enhancing story with LLM")
        
        if not story.text or len(story.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Story text cannot be empty")
        
        # Use the LLM to enhance the story and get title/category
        enhancement_result = enhance_text_with_llm(story.text)
        
        # Create new story with enhanced text, title, and category
        new_story = Story(
            id=str(uuid.uuid4()),
            title=enhancement_result["title"],
            category=enhancement_result["category"],
            text=story.text.strip(),
            enhanced_text=enhancement_result["enhanced_text"].strip(),
            created_at=datetime.now().isoformat(),
            reactions={"funny": 0, "happy": 0, "emotional": 0}
        )

        # Store the story
        stories.append(new_story)
        logger.info(f"Story stored with ID: {new_story.id}, Title: {new_story.title}, Category: {new_story.category}")

        return new_story
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enhancing story: {str(e)}")
        raise HTTPException(status_code=500, detail="Error enhancing story")

@app.get("/stories")
async def get_stories():
    """Get all stories."""
    logger.info(f"Returning {len(stories)} stories")
    return {"stories": stories, "count": len(stories)}

@app.post("/stories/{story_id}/react", response_model=Story)
async def react_to_story(story_id: str, reaction: StoryReaction):
    """Add a reaction to a story."""
    try:
        # Find the story
        story = next((s for s in stories if s.id == story_id), None)
        if not story:
            raise HTTPException(status_code=404, detail="Story not found")

        # Validate reaction type
        valid_reactions = ["funny", "happy", "emotional"]
        if reaction.reaction_type not in valid_reactions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid reaction type. Must be one of: {', '.join(valid_reactions)}"
            )

        # Update the reaction count
        story.reactions[reaction.reaction_type] += 1
        logger.info(f"Added {reaction.reaction_type} reaction to story {story_id}")
        
        return story
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding reaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error adding reaction")

@app.delete("/stories/{story_id}")
async def delete_story(story_id: str):
    """Delete a story."""
    global stories
    original_count = len(stories)
    stories = [s for s in stories if s.id != story_id]
    
    if len(stories) == original_count:
        raise HTTPException(status_code=404, detail="Story not found")
    
    logger.info(f"Deleted story {story_id}")
    return {"message": "Story deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")