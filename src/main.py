from api_key_manager import APIKeyManager
from vision_processor import VisionProcessor

def main() -> None:
    """Main function"""
    try:
        # Initialize API key manager and load key
        api_key = APIKeyManager().load_api_key()
        
        # Initialize vision processor
        processor = VisionProcessor(api_key)
        
        # Process image
        result = processor.analyze_image("../tmp_images/bp-test.png")
        
        # Print results
        print(f"Systolic: {result.systolic}")
        print(f"Diastolic: {result.diastolic}")
        if result.pulse:
            print(f"Pulse: {result.pulse}")
        print(f"Timestamp: {result.timestamp}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
