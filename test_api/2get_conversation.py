import requests

def get_conversation_by_uid(conversation_uid):
    server_ip = "20.167.56.156"
    
    api_url = f"http://{server_ip}:8000/get_conversation/{conversation_uid}"

    # Send a GET request to the get_conversation endpoint
    response = requests.get(api_url)

    # Print the response from the server
    print(response.json())

if __name__ == "__main__":
    # Replace with the conversation UID you want to retrieve
    test_conversation_uid = "9aea2940-041a-4588-b26a-eb49bfa7a3b7"

    # Run the test
    get_conversation_by_uid(test_conversation_uid)
