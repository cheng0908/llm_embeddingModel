import os
import requests

def test_upload_api(file_path, api_url):
    # Extract the original filename from the provided file path
    original_filename = os.path.basename(file_path)

    # Prepare the files dictionary with the original filename
    files = {'file': (original_filename, open(file_path, 'rb'))}

    # Construct the API endpoint URL
    url = f'{api_url}/upload/'

    # Send the POST request with both files and parameters
    response = requests.post(url, files=files)

    # Print the response
    print(response.text)

if __name__ == "__main__":
    # Replace with the actual file path on your Windows machine
    file_path = '.\\elon_musk.txt'
    
    # Replace with the public IP address of your VM
    api_url = 'http://20.167.56.156:8000'

    # Run the test
    test_upload_api(file_path, api_url)