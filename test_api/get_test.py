import requests

def test_get_file(uid):
    server_ip = "20.167.56.156"
    
    api_url = f"http://{server_ip}:8000/get_file/{uid}"
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        with open(f"downloaded_file_{uid}.bin", "wb") as f:
            f.write(response.content)
        print(f"File downloaded successfully for UID: {uid}")
    elif response.status_code == 404:
        print(f"File not found for UID: {uid}")
    else:
        print(f"Error downloading file for UID: {uid}. Status code: {response.status_code}")

if __name__ == "__main__":
    test_uid = "ddc0f3d0-e439-4291-9239-2b645ef66742"
    test_get_file(test_uid)
