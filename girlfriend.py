
import requests
import time
import sys
from ollama import chat

def get_response(prompt, conversation_history):
    conversation_history.append({'role': 'user', 'content': prompt})
    
    stream = chat(
        model='deepseek-r1:1.5b',
        messages=[
            {'role': 'system', 'content': "Act like you are Vanessa, AI girlfriend"}
        ] + conversation_history,
        stream=True,
    )
    
    reasoning_content = ""
    content = ""
    in_thinking = False
    
    for chunk in stream:
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
    
    conversation_history.append({'role': 'assistant', 'content': content})
    
    return content

def generate_talking_avatar(text):
    url = "https://api.d-id.com/talks"

    payload = {
        "source_url": "https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg",
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "Sara"
            },
            "input": text
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer your_key"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        data = response.json()
        talk_id = data.get("id")
        print("talk_id:", talk_id)
        url = f"https://api.d-id.com/talks/{talk_id}"

        headers = {
            "accept": "application/json",
            "authorization": "Bearer your_key"
        }

        time.sleep(10)

        response = requests.get(url, headers=headers)

        if response.status_code == 201:
            data = response.json()
            result_url = data.get("result_url", "No result_url found")
            print("Result URL:", result_url)
            return result_url
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None

def main():
    conversation_history = []
    
    while True:
        user_input = input("\nEnter your query (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting chat...")
            break
        
        # Get AI response
        ai_response = get_response(user_input, conversation_history)
        
        # Generate talking avatar with the AI response
        generate_talking_avatar(ai_response)

if __name__ == "__main__":
    main()



