import ollama
import base64
from pathlib import Path

MODEL_NAME = 'llava'

def encode_image(image_path: str) -> str:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    return base64.b64encode(path.read_bytes()).decode()

def describe_image(image_path: str, question: str = "What's in this image?") -> str:
    try:
        image_b64 = encode_image(image_path)
        response = ollama.chat(model=MODEL_NAME, messages=[
            {"role": "system", "content": "You are a helpful assistant that describes images."},
            {"role": "user", "content": [{"type": "image", "image": image_b64}, {"type": "text", "text": question}]}
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Image Description with Ollama (llava model)\n")
    path = input("Enter image path: ").strip()
    result = describe_image(path)
    print("\n📝 Description:\n" + result)

if __name__ == "__main__":
    main()
