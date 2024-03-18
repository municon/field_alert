import imaplib
import email
from email.header import decode_header
import time
import html2text
import subprocess
import requests
import json
import re
import psutil
import asyncio
import threading

def get_all_ip_addresses():
    addrs = psutil.net_if_addrs()
    ip_list = []
    for interface, addrs in addrs.items():
        for addr in addrs:
            if addr.family == 2:  # AF_INET means IPv4
                if not addr.address.startswith("10.") and not addr.address.startswith("192.168.") and not addr.address.startswith("172."):
                    continue  # Skip loopback and non-LAN IPs
                ip_list.append(addr.address)
    return ip_list

def nmap_find_pdu():
    for ip in ip_list:
        subnet_ip = ".".join(ip.split(".")[:-1]) + "."
        print("CHECKING SUBNET "+ subnet_ip+"0/24 WITH NMAP...\n")
        if subnet_ip == '127.0.0.':
            continue
        # Run nmap and capture the output
        result = ''
        try:
            result = subprocess.run(["nmap", "-sP", f"{subnet_ip}0/24"], capture_output=True, text=True, check=True)
        except subprocess.TimeoutExpired:
            print(f"Timeout expired for subnet {subnet_ip}0/24. Skipping.")
            continue
        except subprocess.CalledProcessError as e:
            if 'unreachable network' in e.stderr:
                print(f"Skipping {subnet_ip}0/24, unreachable network.")
                continue
            else:
                continue  # For other errors, you may choose to do something else
        
        output = result.stdout

        if "can't connect socket:" in output:
            continue

        print(output)

        prev_line=""
        prev_prev_line=""
        for line in output.split("\n"):
            if "98:F0:7B:9E:5F:38" in line:
                # If found, look for the previous line containing IP information
                ip_line = prev_prev_line
                ip_match = re.search(r"for (\d+\.\d+\.\d+\.\d+)", ip_line)
                if ip_match:
                    return ip_match.group(1)
            prev_prev_line = prev_line
            prev_line = line
    print("PDU not found.")
    return None

def get_token():
        # Acquire authorization token
    auth_url = "http://"+pdu_ip+"/services/auth/"
    #auth_payload = json.dumps({"username": "it.support@geopacific.ca", "password": "*4^UnrwlkP"}) LtF#^FBa7Q
    auth_payload = json.dumps({"username": "joseph", "password": "LtF#^FBa7Q"}) 

    auth_headers = {'Content-Type': 'application/json'}

    auth_response = requests.post(auth_url, data=auth_payload, headers=auth_headers)
    if auth_response.status_code != 200 or not auth_response.json()['success']:
        print("Authorization failed.")
        return

    return auth_response.json()['token']

def control_outlet(command, outlets):
    # Control outlet
    token = get_token()

    control_url = f"http://{pdu_ip}/services/control/"
    control_payload = json.dumps({
        "token": token,
        "control": "outlet",
        "command": command,  # "on" or "off"
        "outlets": outlets  # Replace with your outlet number
    })
    control_headers = {'Content-Type': 'application/json'}

    control_response = requests.post(control_url, data=control_payload, headers=control_headers)

    if control_response.status_code == 200 and control_response.json()['success']:
        print(f"Outlet successfully turned {command}")
    else:
        print(f"Failed to turn {command} the outlet: {control_response.json()['message']}. Attempting to refind PDU...\n")
        get_pdu()

def start_timer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(turn_off_outlets_after_delay())

async def turn_off_outlets_after_delay():
    await asyncio.sleep(600)
    control_outlet("off", ['1', '4'])


def check_emails():
    while True:
        try:
            # Initialize connection
            mail = imaplib.IMAP4_SSL("imap.outlook.com")
            mail.login("municon_field_01@outlook.com", "ilovefields123!")

            # Select mailbox
            mail.select("inbox")
            print("Email connection established.")

            # Infinite loop to keep checking for new emails
            while True:
                # Fetch unseen emails
                status, messages = mail.search(None, "UNSEEN")
                new_email_ids = messages[0].split()

                for e_id in new_email_ids:
                    # Fetch email
                    status, msg_data = mail.fetch(e_id, "(RFC822)")

                    for response in msg_data:
                        if isinstance(response, tuple):
                            msg = email.message_from_bytes(response[1])

                            # Decode email sender
                            From, encoding = decode_header(msg.get("From"))[0]
                            if isinstance(From, bytes):
                                From = From.decode(encoding if encoding else "utf-8")
                            
                            if 'joseph@municon.net' in From or 'donotreply@municon.net' in From:

                                # Decode email subject
                                subject, encoding = decode_header(msg["Subject"])[0]
                                if isinstance(subject, bytes):
                                    subject = subject.decode(encoding if encoding else "utf-8")

                                print(f"\n\nNew Email From: {From}\nSubject: {subject}")

                                # Check if the email is multipart
                                if msg.is_multipart():
                                    for part in msg.walk():
                                        # Get MIME type
                                        content_type = part.get_content_type()
                                        # Get content disposition
                                        content_disposition = str(part.get("Content-Disposition"))

                                        content = ""
                                        if "attachment" not in content_disposition and content_type in ["text/plain", "text/html"]:
                                            body = part.get_payload(decode=True).decode().strip()
                                            content = html2text.html2text(body)
                                            #print(content_type.upper()) 

                                        #print("CONTENT: ", content)
                                        pattern = r"value: ([\d\.\-]+)"
                                        match = re.search(pattern, content)
                                        if match:
                                            value = abs(float(match.group(1)))
                                            if(value > 10):
                                                print("AIR HORN!")
                                                control_outlet("on", ['1', '4'])
                                                threading.Thread(target=start_timer).start()

                                            elif(value > 8):
                                                print("LIGHT ON!")
                                                control_outlet("on", ['4'])
                                                threading.Thread(target=start_timer).start()

                                        elif 'OFF' in content:
                                            control_outlet("off", ['1', '4'])

                                            
                # Wait for 10 seconds before checking again
                time.sleep(10)

        except imaplib.IMAP4.abort:  # Server shut down connection
            print("Connection was aborted, attempting to reconnect in 1 minute.")
            time.sleep(60)
            continue
        except imaplib.IMAP4.error:  # Base exception class for all exceptions in imaplib
            print("IMAP error occurred, attempting to reconnect in 1 minute.")
            time.sleep(60)
            continue
        except:  # Socket (WIFI) errors
            print("Socket error occurred: STARLINK is out of range, or WIFI is down. attempting reconnection in 1 minute.")
            time.sleep(60)
            continue

def get_pdu():
    global ip_list
    ip_list = get_all_ip_addresses()
    print("ALL IPS: ", ip_list)

    global pdu_ip 
    pdu_ip = nmap_find_pdu()
    print("PDU IP: ", pdu_ip)

def main():
    get_pdu()
    control_outlet("off", ['1', '4'])
    check_emails()

if __name__ == "__main__":
    main()