from typing import Optional, Union
import base64
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from openai import OpenAI
import yaml

@dataclass
class BPMeasurement:
    """Data class to store blood pressure measurements"""
    systolic: int
    diastolic: int
    pulse: Optional[int] = None
    timestamp: datetime = datetime.now()
    image_path: Optional[str] = None

class ImageProcessingError(Exception):
    """Custom exception for image processing related errors"""
    pass



class VisionProcessor:
    """Processes blood pressure monitor images using OpenAI's Vision API"""
    
    def __init__(
        self, 
        api_key: str,
        prompt_path: Optional[Path] = None,
        model: str = "gpt-4o",
        max_retries: int = 3
    ) -> None:
        """
        Initialize Vision Processor.
        
        Args:
            api_key: OpenAI API key
            prompt_path: Path to YAML file containing system prompt
            model: GPT model to use
            max_retries: Maximum number of API call retries
        """
        if not api_key:
            raise ValueError("API key must be provided")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.prompt_path = prompt_path or Path("config/prompts.yaml")
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        """
        Create the system prompt from YAML configuration.
        
        Returns:
            str: System prompt for image analysis
            
        Raises:
            FileNotFoundError: If prompt configuration file is missing
            ValueError: If prompt configuration is invalid
        """
        try:
            if not self.prompt_path.exists():
                raise FileNotFoundError(f"Prompt configuration not found at: {self.prompt_path}")
                
            with open(self.prompt_path, 'r') as f:
                config = yaml.safe_load(f)
                
            if 'vision_prompt' not in config:
                raise ValueError("Missing 'vision_prompt' in configuration")
                
            return config['vision_prompt']
            
        except Exception as e:
            # Fallback to default prompt if configuration fails
            return (
                "Please analyze this blood pressure monitor image and extract:\n"
                "1. Systolic pressure \n"
                "2. Diastolic pressure \n"
                "3. Pulse rate \n\n"
                "Return only these numbers in format: systolic/diastolic/pulse\n"
                "If any value is not visible, use 'None' for that position."
            )

    def encode_image(self, image_path: Union[str, Path]) -> str:
        """Encode image to base64 string."""
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found at: {image_path}")
                
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
                
        except Exception as e:
            raise ImageProcessingError(f"Failed to encode image: {str(e)}")

    def analyze_image(self, image_path: Union[str, Path]) -> BPMeasurement:
        """Process blood pressure monitor image and extract measurements."""
        try:
            base64_image = self.encode_image(image_path)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.system_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            return self._parse_response(
                response.choices[0].message.content,
                str(image_path)
            )
            
        except Exception as e:
            raise ImageProcessingError(f"Failed to analyze image: {str(e)}")

    def _parse_response(self, response: str, image_path: str) -> BPMeasurement:
        """Parse API response into BPMeasurement object."""
        try:
            values = response.strip().split('/')
            
            systolic = int(values[0]) if values[0] != 'None' else None
            diastolic = int(values[1]) if values[1] != 'None' else None
            pulse = int(values[2]) if len(values) > 2 and values[2] != 'None' else None
            
            if not self._validate_readings(systolic, diastolic, pulse):
                raise ValueError("Invalid blood pressure readings detected")
            
            return BPMeasurement(
                systolic=systolic,
                diastolic=diastolic,
                pulse=pulse,
                image_path=image_path
            )
            
        except Exception as e:
            raise ValueError(f"Failed to parse response: {str(e)}")

    def _validate_readings(
        self,
        systolic: Optional[int],
        diastolic: Optional[int],
        pulse: Optional[int]
    ) -> bool:
        """Validate blood pressure readings."""
        if not (systolic and diastolic):
            return False
            
        if not (60 <= systolic <= 250 and 40 <= diastolic <= 130):
            return False
            
        if systolic <= diastolic:
            return False
            
        if pulse is not None and not (40 <= pulse <= 200):
            return False
            
        return True
