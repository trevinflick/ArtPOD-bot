from atproto import Client
from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

def fetch_art_data_from_github():
    github_url = "https://raw.githubusercontent.com/trevinflick/fetch_art/main/art_data.json"
    response = requests.get(github_url)
    response.raise_for_status()  # Check for request errors
    data = response.json()  # Parse the JSON data

    # Extract data from JSON
    image_url = data.get("image_url", "No image available")
    description = data.get("description", "No description available")
    artist_display = data.get("artist_info", "No artist information available")
    title = data.get("title", "No title available")
    alt_text = data.get("alt_text", "No alternative text available")  # Fetch alt_text field
    
    return image_url, description, artist_display, title, alt_text

def download_image(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    filename = "art_image.jpg"
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

def post_to_bluesky(image_path, text, alt_text):
    # Initialize the Bluesky client with environment variables for security
    bluesky_handle = os.getenv("BLUESKY_HANDLE")
    bluesky_password = os.getenv("BLUESKY_PASSWORD")
    client = Client()
    client.login(bluesky_handle, bluesky_password)

    # Read image data
    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()

    # Send post with image
    try:
        client.send_image(text=text, image=img_data, image_alt=alt_text)
        print("Post created successfully on Bluesky.")
    except Exception as e:
        print(f"Error posting to Bluesky: {e}")

def main():
    # Fetch the art data
    image_url, description, artist_display, title, alt_text = fetch_art_data_from_github()

    # Download the image
    image_path = download_image(image_url)

    # Create the post text
    post_text = f"{title}\n{artist_display}"

    # Use description as alt text if alt_text is "No alternative text available"
    image_alt_text = alt_text if alt_text != "No alternative text available" else description

    # Post to Bluesky
    post_to_bluesky(image_path, post_text, image_alt_text)

    # Clean up: delete the downloaded image
    os.remove(image_path)

if __name__ == "__main__":
    main()
