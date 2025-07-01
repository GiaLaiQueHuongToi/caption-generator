"""
WhisperX service for speech recognition and transcription.
"""
import whisperx
import torch
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..models.subtitle import TranscriptSegment
from ..core.config import settings


class WhisperXService:
    def __init__(self):
        # Force CPU usage if CUDA_VISIBLE_DEVICES is set to empty
        import os
        if os.getenv("CUDA_VISIBLE_DEVICES") == "":
            self.device = "cpu"
            print("Forcing CPU usage due to CUDA_VISIBLE_DEVICES environment variable")
        else:
            # Check CUDA availability more safely
            try:
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            except Exception as e:
                print(f"CUDA check failed, falling back to CPU: {e}")
                self.device = "cpu"
        
        self.compute_type = "float16" if self.device == "cuda" else "int8"
        self.model = None
        self.align_model = None
        self.metadata = None
        print(f"WhisperX will use device: {self.device}")
        
    async def load_model(self):
        """Load WhisperX model if not already loaded"""
        if self.model is None:
            print(f"Loading WhisperX model: {settings.whisperx.model}")
            try:
                self.model = whisperx.load_model(
                    settings.whisperx.model, 
                    self.device, 
                    compute_type=self.compute_type,
                    language=None  # Let it auto-detect
                )
            except Exception as e:
                print(f"Error loading model with device {self.device}, trying CPU fallback: {e}")
                
                # If CUDA failed, try CPU
                if self.device == "cuda":
                    print("Falling back to CPU due to CUDA issues")
                    self.device = "cpu"
                    self.compute_type = "int8"
                    
                    try:
                        self.model = whisperx.load_model(
                            settings.whisperx.model, 
                            self.device, 
                            compute_type=self.compute_type,
                            language=None
                        )
                    except Exception as e2:
                        print(f"CPU fallback with new API failed, trying basic loading: {e2}")
                        # Final fallback to basic loading
                        self.model = whisperx.load_model(
                            settings.whisperx.model, 
                            self.device
                        )
                else:
                    # Already on CPU, try basic loading
                    print("Trying basic model loading without extra parameters")
                    self.model = whisperx.load_model(
                        settings.whisperx.model, 
                        self.device
                    )
    
    async def transcribe_video(self, video_path: Path) -> Dict[str, Any]:
        """Transcribe video and return word-level timestamps"""
        await self.load_model()
        
        # Load audio from video
        audio = whisperx.load_audio(str(video_path))
        
        # Try different transcription approaches based on WhisperX version
        try:
            # Try with new API parameters first
            result = self.model.transcribe(
                audio, 
                batch_size=16,
                language=None
            )
        except TypeError as e:
            if "missing" in str(e) and "required positional arguments" in str(e):
                print("Detected newer WhisperX API, using updated parameters...")
                # Use the newer API with all required parameters
                result = self.model.transcribe(
                    audio,
                    batch_size=16,
                    language=None,
                    multilingual=True,
                    max_new_tokens=448,  # Default value
                    clip_timestamps="0,30",  # Default clip range
                    hallucination_silence_threshold=None,
                    hotwords=None
                )
            else:
                raise e
        
        # Load alignment model for detected language
        language = result.get("language", "en")
        print(f"Detected language: {language}")
        
        # Try to align whisper output for better word-level timestamps
        try:
            align_model, metadata = whisperx.load_align_model(
                language_code=language, 
                device=self.device
            )
            
            # Align whisper output
            aligned_result = whisperx.align(
                result["segments"], 
                align_model, 
                metadata, 
                audio, 
                self.device, 
                return_char_alignments=False
            )
        except Exception as e:
            print(f"Warning: Alignment failed ({e}), using original segments")
            # Fall back to using original segments without alignment
            aligned_result = {"segments": result["segments"]}
        
        return {
            "language": language,
            "segments": aligned_result["segments"],
            "word_segments": aligned_result.get("word_segments", [])
        }
    
    def group_words_into_captions(self, segments: List[Dict]) -> List[TranscriptSegment]:
        """Group words into readable caption segments of 6-7 words"""
        captions = []
        current_words = []
        current_start = None
        current_end = None
        
        for segment in segments:
            # Handle segments with word-level timestamps
            if "words" in segment and segment["words"]:
                for word in segment["words"]:
                    if "start" not in word or "end" not in word:
                        continue
                        
                    # Start new caption if this is the first word
                    if current_start is None:
                        current_start = word["start"]
                    
                    current_words.append(word["word"].strip())
                    current_end = word["end"]
                    
                    # Create caption when we have enough words or reached max duration
                    should_create_caption = (
                        len(current_words) >= settings.whisperx.words_per_caption or
                        (current_end - current_start) >= settings.whisperx.max_caption_duration
                    )
                    
                    if should_create_caption and len(current_words) >= settings.whisperx.min_words_per_caption:
                        caption_text = " ".join(current_words).strip()
                        if caption_text:
                            captions.append(TranscriptSegment(
                                start=current_start,
                                end=current_end,
                                text=caption_text
                            ))
                        
                        # Reset for next caption
                        current_words = []
                        current_start = None
                        current_end = None
            
            # Fallback: Handle segments without word-level timestamps
            elif "text" in segment and "start" in segment and "end" in segment:
                text = segment["text"].strip()
                if text:
                    # Split long segments into smaller captions
                    words = text.split()
                    start_time = segment["start"]
                    end_time = segment["end"]
                    duration = end_time - start_time
                    
                    # Create captions from word chunks
                    for i in range(0, len(words), settings.whisperx.words_per_caption):
                        chunk_words = words[i:i + settings.whisperx.words_per_caption]
                        chunk_text = " ".join(chunk_words)
                        
                        # Calculate timing for this chunk
                        chunk_start = start_time + (i / len(words)) * duration
                        chunk_end = start_time + ((i + len(chunk_words)) / len(words)) * duration
                        
                        captions.append(TranscriptSegment(
                            start=chunk_start,
                            end=chunk_end,
                            text=chunk_text
                        ))
        
        # Add remaining words as final caption (for word-level processing)
        if current_words and current_start is not None:
            caption_text = " ".join(current_words).strip()
            if caption_text:
                captions.append(TranscriptSegment(
                    start=current_start,
                    end=current_end,
                    text=caption_text
                ))
        
        return captions
    
    def create_srt_content(self, captions: List[TranscriptSegment]) -> str:
        """Convert caption segments to SRT format"""
        srt_content = ""
        
        for i, caption in enumerate(captions, 1):
            start_time = self._seconds_to_srt_time(caption.start)
            end_time = self._seconds_to_srt_time(caption.end)
            
            srt_content += f"{i}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{caption.text}\n\n"
        
        return srt_content
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
