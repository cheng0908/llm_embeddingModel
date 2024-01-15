import requests

def test_save_conversation(conversation_uid, chat_content_result):
    server_ip = "20.167.56.156"
    
    api_url = f"http://{server_ip}:8000/save_conversation/"
    
    # Send a POST request to the save_conversation endpoint
    response = requests.post(api_url, json={"conversation_uid": conversation_uid, "chat_content_result": chat_content_result})

    # Print the response from the server
    print(response.json())

if __name__ == "__main__":
    # Replace with the conversation UID and chat content result you want to test
    test_conversation_uid = "9aea2940-041a-4588-b26a-eb49bfa7a3b7"
    test_chat_content_result = "Hi, your_chat_content_result, 9aea2940-041a-4588-b26a-eb49bfa7a3b7"

    # Run the test
    test_save_conversation(test_conversation_uid, test_chat_content_result)
