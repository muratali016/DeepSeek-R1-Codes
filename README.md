# Udemy Deepseek Work
# DeepSeek-R1 local image upload

# DeepSeek-R1-Girlfriend
This project integrates the locally installed **Deepseek-R1 (1.5B)** model with the **D-ID API** to create an interactive AI girlfriend chatbot named Vanessa. The chatbot generates responses and converts them into a talking avatar using **D-ID's API**.

## Features
- Local AI chatbot using Deepseek-R1 (1.5B)
- Chat history management
- Integration with D-ID API to generate a talking avatar

## Installation
1. Install dependencies:
   ```sh
   pip install requests ollama
   ```
2. Install and set up **Deepseek-R1 (1.5B)** locally using Ollama:
   ```sh
   ollama pull deepseek-r1:1.5b
   ```

## Usage
1. Replace `your_key` in the `generate_talking_avatar` function with your D-ID API key.
2. Run the chatbot:
   ```sh
   python main.py
   ```
3. Enter prompts to chat with Vanessa. The AI-generated response will be converted into a talking avatar using the D-ID API.

## API Requirements
- **Deepseek-R1 (1.5B)** (via Ollama)
- **D-ID API** (Requires an API key)

## Notes
- The D-ID API uses a default image (`alice.jpg`) and Microsoft’s `Sara` voice.
- Adjust the `source_url` and voice settings in the `generate_talking_avatar` function as needed.


D-ID API (Requires an API key)

Notes

The D-ID API uses a default image (alice.jpg) and Microsoft’s Sara voice.

Adjust the source_url and voice settings in the generate_talking_avatar function as needed.
