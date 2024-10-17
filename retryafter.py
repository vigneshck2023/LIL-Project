import requests

def get_retry_after(url):
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            # Process the response data as needed
            print(response.text)
        elif response.status_code == 429:
            if 'Retry-After' in response.headers:
                retry_after = response.headers['Retry-After']
                print(f"Retry-After: {retry_after}")
                # You can use the 'retry_after' value here for further handling
                
            else:
                print("Retry-After header not found")
                
        else:
            print(f"Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Usage example
website_url = "https://example.com"

get_retry_after(website_url)
