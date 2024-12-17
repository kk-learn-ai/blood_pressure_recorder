# Blood Pressure Web Monitoring (BPWM)
A web application that allows users to capture and record blood pressure measurements through photo recognition.

## Project Overview
BPWM is a Python-based application that leverages OpenAI's GPT-4 Vision capabilities to accurately extract blood pressure readings from monitor photos. The system processes images to detect systolic pressure, diastolic pressure, and pulse rate measurements.

Features (v1.0)
- Automated extraction of blood pressure readings from photos
- Support for multiple blood pressure monitor types
- Validation of extracted measurements
- Error handling 
- Base64 image encoding
- Secure API key management
- Timestamp tracking for measurements

    
## Technical Stack

### Backend:
- Python 3.9+
- OpenAI GPT-4 Vision API
- Dependencies from requirements.txt

## Dependencies
```
openai>=1.3.0
python-dotenv>=1.0.0
pyyaml>=6.0.1
```

## Installation

1. Clone the repository:
```
git clone https://github.com/kk-learn-ai/blood_pressure_recorder.git
cd blood_pressure_recorder
```

2. Create Conda Environment
```
conda create --name bpr python
conda activate bpr
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Configure environment:
```
cp .env.example .env
# Replace your OpenAI API key accordingly in the .env file
```

## Project Structure
blood_pressure_recorder/
├── config/
│   └── prompts.yaml         # System prompts configuration
├── src/
│   ├── vision_processor.py  # Core vision processing logic
│   ├── api_key_manager.py   # API key management
│   └── main.py             # Application entry point
├── tmp_images/             # Directory for temporary image storage
├── .env                    # Environment variables and API keys
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation


## Error Handling
The system includes error handling for:
- Invalid API keys
- Missing or corrupt image files
- Failed image processing
- Invalid blood pressure readings
- API communication errors

## Measurement Validation
Blood pressure readings are validated against these ranges:
- Systolic: 60-250 mmHg
- Diastolic: 40-130 mmHg
- Pulse: 40-200 BPM

## Running the Application

1. Run the main script:

```bash
python src/main.py
```

2. To process a different image, modify the image path in main.py:

```python
result = processor.analyze_image("path/to/your/image.jpg")
```

## Customizing System Prompt

1. Navigate to `config/prompts.yaml`

2. Modify the vision prompt according to your needs:

```text
vision_prompt: |
  Please analyze this blood pressure monitor image and extract:
  1. Systolic pressure 
  2. Diastolic pressure 
  3. Pulse rate 

  Return only these numbers in format: systolic/diastolic/pulse
  If any value is not visible, use 'None' for that position.
```

3. The prompt must maintain the output format systolic/diastolic/pulse for proper parsing

4. Save the file and restart the application for changes to take effect

Note: If the YAML file is missing or invalid, the system will fall back to the default prompt defined in the VisionProcessor class.

## Future Enhancements
- Web interface for image upload
- User authentication
- Reading history and trends
- Report generation
- Notification to contacts
- Cloud storage integration

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Project Maintainer: kk