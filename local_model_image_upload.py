import os
import sys
import re
import base64
from dotenv import load_dotenv
from ollama import chat
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="sk--"  # Replace with your actual API key
)

conversation_history = []

def detect_file_path(text):
    """
    Detects and extracts file paths from input text, including paths within quotes or natural language.
    """
    file_patterns = [
        
        r'"([^"]+\.(png|jpg|jpeg|gif|bmp|tiff))"',
        r'\'([^\']+\.(png|jpg|jpeg|gif|bmp|tiff))\'',
        
        
        r'(?:^|\s)([\/\\]?(?:[a-zA-Z]:)?[\/\\]?(?:[\w\-\s\.]+[\/\\])*[\w\-\s]+\.(png|jpg|jpeg|gif|bmp|tiff))(?:\s|$)',
        
        
        r'(?:image|file|path)[:\s]+([\/\\]?(?:[a-zA-Z]:)?[\/\\]?(?:[\w\-\s\.]+[\/\\])*[\w\-\s]+\.(png|jpg|jpeg|gif|bmp|tiff))'
    ]
    
    for pattern in file_patterns:
        matches = re.search(pattern, text, re.IGNORECASE)
        if matches:
            path = matches.group(1)
            path = path.strip()
            path = os.path.normpath(path)
            return path
            
    return None

def encode_image(image_path):
    """
    Encodes an image file to base64 string.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return None

def analyze_image(image_path):
    """
    Analyzes an image using OpenAI's vision API.
    """
    try:
        base64_image = encode_image(image_path)
        if not base64_image:
            return "Error: Could not encode image"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please describe this image and extract any text you see in it.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error processing image: {str(e)}"

def is_valid_file_path(path):
    """
    Checks if the given path is a valid file.
    """
    return os.path.isfile(path)

def process_user_input(user_input):
    """
    Processes user input to detect and validate file paths.
    """
    file_path = detect_file_path(user_input)
    if file_path and is_valid_file_path(file_path):
        return file_path
    return None

def main():
    print("Start chatting with the AI (type 'quit' to exit):")
    print("You can also send image files for analysis!")
    audio_enabled = True
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        elif user_input.lower() == 'mute':
            audio_enabled = not audio_enabled
            print(f"Audio {'enabled' if audio_enabled else 'disabled'}")
            continue
            
        # Check for file paths in the input
        file_path = process_user_input(user_input)
        image_analysis = None
        
        if file_path:
            print("\nAnalyzing image...")
            image_analysis = analyze_image(file_path)
            if image_analysis:
                print("\nImage Analysis:\n", image_analysis)
                user_input = f"Image analysis: {image_analysis}"
            else:
                print("No content could be extracted from the image.")
        
        
        conversation_history.append({'role': 'user', 'content': user_input})
        reasoning_content = ""
        content = ""
        in_thinking = False
        full_response = ""
        
        try:
            stream_chat = chat(
                model='deepseek-r1:1.5b',
                messages=conversation_history,
                stream=True,
            )
            
            print("\nAI: ", end='')
            
            for chunk in stream_chat:
                if chunk and 'message' in chunk and chunk['message'].content:
                    chunk_content = chunk['message'].content
                    sys.stdout.write(chunk_content)
                    sys.stdout.flush()
                    
                    if chunk_content.startswith('<think>'):
                        in_thinking = True
                    elif chunk_content.startswith('</think>'):
                        in_thinking = False
                    else:
                        if in_thinking:
                            reasoning_content += chunk_content
                        else:
                            content += chunk_content
                            full_response += chunk_content
            
            if reasoning_content:
                print("\n\nReasoning:", reasoning_content)
            if content:
                print("\nFinal Answer:", content)
                

            conversation_history.append({'role': 'assistant', 'content': full_response})
            
        except Exception as e:
            print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    main()
