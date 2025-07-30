import json
import random
import time
import threading
import tls_client
import string
import re
import websocket
import requests
from colorama import Fore

class View:
    def __init__(self, arg):
        self.username = arg
        self.channel_id = None
        self.UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        self.client_token = "e1393935a959b4020a4491574f6490129f678acdaa92760471263db43487f823"

        self.session = tls_client.Session(
            client_identifier="chrome120",
            random_tls_extension_order=True
        )

        try:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.UserAgent,
                'sec-ch-ua': '"Chromium";v="137", "Google Chrome";v="137", "Not-A.Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            response = self.session.get(f'https://kick.com/api/v2/channels/{arg}', headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.channel_id = data.get('id')
                if not self.channel_id:
                    print(f"Failed to get channel ID for {arg}")
            else:
                print(f"Failed to get channel info for {arg}: {response.status_code}")
        except Exception as e:
            print(f"Error initializing View for {arg}: {e}")

    def get_token(self, proxy_dict=None):
        try:
            session = tls_client.Session(client_identifier="chrome120", random_tls_extension_order=True)
            session.headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.UserAgent,
                'sec-ch-ua': '"Chromium";v="137", "Google Chrome";v="137", "Not-A.Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            if proxy_dict:
                session.proxies = proxy_dict

            session.get("https://kick.com")
            session.headers["X-CLIENT-TOKEN"] = self.client_token
            response = session.get('https://websockets.kick.com/viewer/v1/token')

            if response.status_code == 200:
                return response.json()["data"]["token"]
            else:
                print(f"Failed to get token: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting token: {e}")
            return None

    def send_view_websocket(self, token, channel_id, end_time, proxy_dict=None):
        try:
            ws = websocket.WebSocket()

            if proxy_dict and 'http' in proxy_dict:
                proxy_url = proxy_dict['http']
                if '@' in proxy_url:
                    auth_part = proxy_url.split('@')[0].replace('http://', '')
                    host_port = proxy_url.split('@')[1]
                    user, password = auth_part.split(':')
                    host, port = host_port.split(':')
                    ws.connect(
                        f"wss://websockets.kick.com/viewer/v1/connect?token={token}",
                        header=[
                            f"User-Agent: {self.UserAgent}",
                            "Origin: https://kick.com",
                            f"Cookie: client_token={self.client_token}"
                        ],
                        http_proxy_host=host,
                        http_proxy_port=int(port),
                        http_proxy_auth=(user, password)
                    )
                else:
                    host_port = proxy_url.replace('http://', '')
                    host, port = host_port.split(':')
                    ws.connect(
                        f"wss://websockets.kick.com/viewer/v1/connect?token={token}",
                        header=[
                            f"User-Agent: {self.UserAgent}",
                            "Origin: https://kick.com",
                            f"Cookie: client_token={self.client_token}"
                        ],
                        http_proxy_host=host,
                        http_proxy_port=int(port)
                    )
            else:
                ws.connect(
                    f"wss://websockets.kick.com/viewer/v1/connect?token={token}",
                    header=[
                        f"User-Agent: {self.UserAgent}",
                        "Origin: https://kick.com",
                        f"Cookie: client_token={self.client_token}"
                    ]
                )

            x = 0
            while time.time() < end_time:
                x += 1
                if x % 2 == 0:
                    ws.send(json.dumps({"type": "ping"}))
                    print(f"Sent ping for {self.username}")
                else:
                    ws.send(json.dumps({
                        "type": "channel_handshake",
                        "data": {
                            "message": {"channelId": channel_id}
                        }
                    }))
                    print(f"Sent handshake for {self.username}")

                sleep_time = 12 + random.randint(1, 5)
                time.sleep(sleep_time)

            print(f"[EXIT] View time expired for {self.username}")
            ws.close()
            return True

        except Exception as e:
            print(f"Error in websocket view for {self.username}: {e}")
            return False

    def Send(self, proxies, arg, end_time):
        if not self.channel_id:
            print(f"No channel ID available for {arg}")
            return False

        try:
            if proxies is None:
                proxy_dict = None
                print(f"Using direct connection for {arg}")
            elif isinstance(proxies, dict):
                proxy_dict = proxies
            else:
                if '@' in proxies:
                    proxy_dict = {
                        'http': f'http://{proxies}',
                        'https': f'http://{proxies}'
                    }
                else:
                    proxy_dict = {
                        'http': f'http://{proxies}',
                        'https': f'http://{proxies}'
                    }
                print(f"Using proxy: {proxies}")

            token = self.get_token(proxy_dict)
            if not token:
                print(f"Failed to get token for {arg}")
                return False

            print(f"Got token for {arg}: {token}")
            success = self.send_view_websocket(token, self.channel_id, end_time, proxy_dict)

            if success:
                print(f"View session completed for {arg}")
                return True
            else:
                print(f"Failed to send view for {arg}")
                return False

        except Exception as e:
            print(f"Error in View.Send for {arg}: {e}")
            return False
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
import json
import requests
import tls_client
from colorama import Fore

class Follow:
    def __init__(self):
        # Connection pool for better performance
        self.session_pool = {}
        self.session_lock = threading.Lock()
        
        # Token cache to reduce file I/O
        self.token_cache = []
        self.token_cache_lock = threading.Lock()
        self.cache_loaded = False
        
        # Proxy cache
        self.proxy_cache = []
        self.proxy_cache_lock = threading.Lock()
        self.proxy_cache_loaded = False
        
        self.account_unlocked = False
        self.lock = threading.Lock()

    def load_tokens_cache(self):
        """Load tokens into memory cache to reduce file I/O"""
        if not self.cache_loaded:
            with self.token_cache_lock:
                if not self.cache_loaded:
                    try:
                        with open(r"C:\Users\Administrator\Desktop\private bot system\data\kick.txt", "r") as f:
                            self.token_cache = f.read().splitlines()
                        self.cache_loaded = True
                    except Exception as e:
                        print(f"[ ERROR ] Failed to load token cache: {e}")
                        return []
        return self.token_cache

    def load_proxy_cache(self):
        """Load proxies into memory cache"""
        if not self.proxy_cache_loaded:
            with self.proxy_cache_lock:
                if not self.proxy_cache_loaded:
                    try:
                        with open(r"C:\Users\Administrator\Desktop\private bot system\data\proxy.txt", "r") as f:
                            self.proxy_cache = f.read().splitlines()
                        self.proxy_cache_loaded = True
                    except Exception as e:
                        print(f"[ ERROR ] Failed to load proxy cache: {e}")
                        return []
        return self.proxy_cache

    def get_session(self, proxy):
        """Get or create a session for a specific proxy to enable connection pooling"""
        with self.session_lock:
            if proxy not in self.session_pool:
                proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                self.session_pool[proxy] = tls_client.Session(
                    client_identifier=f"chrome127", 
                    random_tls_extension_order=True, 
                    ja3_string=",".join([
                        "771", 
                        "-".join([str(random.randint(50, 52392)) for _ in range(15)]), 
                        "-".join("45-16-23-65281-35-65037-51-10-43-13-17513-5-0-11-18-27".split("-")), 
                        "29-23-24,0"
                    ])
                )
            return self.session_pool[proxy]

    def get_new_token_optimized(self):
        """Optimized token retrieval with caching"""
        tokens = self.load_tokens_cache()
        if not tokens:
            return None
        
        with self.lock:
            if tokens:
                line = tokens.pop(random.randint(0, len(tokens)-1))
                return line.strip()
        return None

    def unlockAccount(self, user, amount):
        try:
            # Load caches
            proxies = self.load_proxy_cache()
            if not proxies:
                print(f"{Fore.RED}[Error] No proxies available{Fore.RESET}")
                return
            
            # Get initial proxy and session
            proxy = random.choice(proxies)
            session = self.get_session(proxy)
            
            headers = {
                 "authority": "kick.com",
                 "accept": "application/json, text/plain, */*",
                 "accept-language": "en-US",
                 "referer": "https://kick.com/",
                 "sec-ch-ua": f'"Chromium";v="127", "Not(A:Brand";v="127", "Google Chrome";v="127"',
                 "sec-ch-ua-mobile": "?0",
                 "sec-ch-ua-platform": '"Windows"',
                 "sec-fetch-dest": "empty",
                 "sec-fetch-mode": "cors",
                 "sec-fetch-site": "same-origin",
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            }

            response = session.get(f'https://kick.com/api/v2/channels/{user}', headers=headers, proxy={'http': f'http://{proxy}', 'https': f'http://{proxy}'})
            user_id = response.json()["id"]
            self.account_unlocked = True
            
            # Use optimized ThreadPoolExecutor for concurrent follows
            success_count = 0
            max_workers = min(20, amount)  # Limit concurrent threads
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(self.followAccount_optimized, user_id) for _ in range(amount)]
                
                # Process results with progress tracking
                for future in as_completed(futures):
                    if future.result():
                        success_count += 1
                    
                    # Small delay to prevent overwhelming
                    if success_count % 10 == 0:
                        time.sleep(0.1)

            print(f"{Fore.GREEN}[Complete] Successfully sent {success_count}/{amount} follows{Fore.RESET}")

        except Exception as e:
            print(f"{Fore.RED}[Error] UnlockAccount: {str(e)}{Fore.RESET}")

    def followAccount_optimized(self, user_id):
        """Optimized follow account method with better error handling"""
        if not self.account_unlocked:
            print(f"{Fore.YELLOW}[Warning] Account not unlocked yet{Fore.RESET}")
            return False
            
        token = self.get_new_token_optimized()
        if not token:
            print(f"{Fore.RED}[Error] No tokens available{Fore.RESET}")
            return False
        
        # Get proxy and session
        proxies = self.load_proxy_cache()
        if not proxies:
            return False
            
        proxy = random.choice(proxies)
        session = self.get_session(proxy)
        
        try:    
            url = "https://kick.com/api/v1/channels/user/subscribe"
            headers = {
                 "authority": "kick.com",
                 "accept": "application/json, text/plain, */*",
                 "authorization": f"Bearer {token}",
                 "content-type": "application/json",
                 "accept-language": "en-US",
                 "referer": "https://kick.com/",
                 "sec-ch-ua": f'"Chromium";v="126", "Not(A:Brand";v="126", "Google Chrome";v="126"',
                 "sec-ch-ua-mobile": "?0",
                 "sec-ch-ua-platform": '"Windows"',
                 "sec-fetch-dest": "empty",
                 "sec-fetch-mode": "cors",
                 "sec-fetch-site": "same-origin",
                 "x-xsrf-token": token,
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            }
            payload = {
                "channel_id": user_id
            }
            
            res = session.post(url, headers=headers, json=payload, cookies={"x-xsrf-token": token}, proxy={'http': f'http://{proxy}', 'https': f'http://{proxy}'})
            
            if res.status_code == 201:
                print(f"{Fore.GREEN}[Success] Follow successful | Token: {token}{Fore.RESET}")
                return True
            else:
                print(f"{Fore.YELLOW}[Warning] Status code: {res.status_code} | Token: {token}{Fore.RESET}")
                return False

        except requests.exceptions.Timeout as e:
            print(f"{Fore.RED}[Timeout Error] {str(e)} | Token: {token}{Fore.RESET}")
            return False

        except Exception as e:
            if str(e) == "Expecting value: line 1 column 1 (char 0)":
                print(f"{Fore.RED}[Error] Token banned | Token: {token}{Fore.RESET}")
            else:
                print(f"{Fore.RED}[Error] FollowAccount: {str(e)} | Token: {token}{Fore.RESET}")
            return False

    # Keep original method for backward compatibility
    def followAccount(self, user_id):
        return self.followAccount_optimized(user_id)




class Chat:
    def __init__(self):
        self.session = tls_client.Session(
            client_identifier=f"chrome127", 
            random_tls_extension_order=True, 
            ja3_string=",".join([
                "771", 
                "-".join([str(random.randint(50, 52392)) for _ in range(15)]), 
                "-".join("45-16-23-65281-35-65037-51-10-43-13-17513-5-0-11-18-27".split("-")), 
                "29-23-24,0"
            ])
        )
        
    def get_random_token(self):
        """Get random token from kick.txt file (one token per line)"""
        with open(r"C:\Users\Administrator\Desktop\private bot system\data\kick.txt", "r") as f:
            lines = f.read().splitlines()
            if not lines:
                raise Exception("No tokens found in kick.txt")
            token = random.choice(lines)
            return token.strip(), None  # Username is None

    def unlockAccount(self, username, message, min_delay, max_delay, amount):
        print("chat")
        
        self.proxy = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\proxy.txt","r").read().splitlines())
        self.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'}
        
        # Get initial token and username
        self.token, self.bot_username = self.get_random_token()
        self.user = username

        self.message_initial = message
        self.message = message
        
        self.words = []
        self.min_delay = min_delay
        self.max_delay = max_delay
        if self.message_initial:
            if "pastebin.com" in self.message_initial:
                prefix = self.message_initial[:self.message_initial.find(".com")+5]
                sufix = self.message_initial[self.message_initial.find(".com")+5:]
                link = prefix + "raw/" + sufix
                r = requests.get(link)
                for line in r.text.splitlines():
                    self.words.append(line.strip())
                self.message = self.words
        if len(self.words) != 0:
            self.message = random.choice(self.words)
        try:
            headers = {
                 "authority": "kick.com",
                 "accept": "application/json, text/plain, */*",
                 "accept-language": "en-US",
                 "referer": "https://kick.com/",
                 "sec-ch-ua": f'"Chromium";v="127", "Not(A:Brand";v="127", "Google Chrome";v="127"',
                 "sec-ch-ua-mobile": "?0",
                 "sec-ch-ua-platform": '"Windows"',
                 "sec-fetch-dest": "empty",
                 "sec-fetch-mode": "cors",
                 "sec-fetch-site": "same-origin",
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            }

            response = self.session.get(f'https://kick.com/api/v2/channels/{self.user}/chatroom', headers=headers, proxy=self.proxies)
            self.chatroom_id = response.json()["id"]
            self.account_unlocked = True
            if(self.account_unlocked): 
                with ThreadPoolExecutor(max_workers=10) as executor:  
                    futures = [executor.submit(self.send_message) for _ in range(amount)]
                    # for future in futures:
                    #     if future.result():
                    #         success_count += 1
        except Exception as e:
            print(e)


    def send_message(self):
        proxy = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\proxy.txt","r").read().splitlines())
        proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'}
        delay = self.sleep_time(self.min_delay, self.max_delay)
        time.sleep(delay)
        
        # Get new token and username for each message
        token, username = self.get_random_token()

        headers = {
            "authority": "kick.com",
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "accept-language": "en-US",
            "referer": "https://kick.com/",
            "sec-ch-ua": f'"Chromium";v="127", "Not(A:Brand";v="127", "Google Chrome";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-xsrf-token": token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }

        data = {"content": self.message, "type": "message"}
        print(f"Sending message as {username}: {self.message}")
        
        try:
            response = self.session.post(
                f"https://kick.com/api/v2/messages/send/{self.chatroom_id}",
                headers=headers,
                cookies={"x-xsrf-token": token},
                json=data,
                proxy=proxies,
            )
            if response.status_code == 200:
                response_json = response.json()
                if response_json["status"]["error"]:
                    print(f"Message sending error: {response_json['status']['message']}")
                else:
                    print(f"Message sent successfully {token}")
            elif response.status_code == 400 and str('FOLLOWERS_ONLY') in str(response.text):
                print(f"Followers Mode ONLY: {self.chatroom_id} | Token: {token}")
            elif response.status_code == 400 and str('banned') in str(response.text):
                print(f"Token is banned: {token}")
            elif response.status_code == 400:
                print(f"Other Error: {token} // JSON: {response.text}")
            elif response.status_code == 403:
                print("Cloudflare detected: Cooldown initiated.")
            elif response.status_code == 500:
                print(f"Server Error: {response.text}")
            else:
                print(f"Unknown response: {response.status_code} - {response.text}")

        except Exception as error:
            print(f"Error when sending message: {error}", exc_info=True)

    def sleep_time(self, min, max):
        number = random.uniform(min, max)
        print(f"Sleeping for {number} seconds...")
        return number
    


class Clip:
    def __init__(self, clip_id):
        self.session = tls_client.Session(client_identifier=f"chrome127", random_tls_extension_order=True, ja3_string=",".join(["771", "-".join([str(random.randint(50, 52392)) for _ in range(15)]), "-".join("45-16-23-65281-35-65037-51-10-43-13-17513-5-0-11-18-27".split("-")), "29-23-24,0"]))
        self.proxy = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\proxy.txt","r").read().splitlines())
        self.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'}
        self.token = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\kick.txt","r").read().splitlines())
        self.clip_id = clip_id 

    def send_view(self):

        headers = {
            "authority": "kick.com",
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {self.token}",
            "content-type": "application/json",
            "accept-language": "en-US",
            "referer": "https://kick.com/",
            "sec-ch-ua": f'"Chromium";v="127", "Not(A:Brand";v="127", "Google Chrome";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-xsrf-token": self.token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }

        try:
            response = self.session.get(
                f"https://kick.com/api/v2/clips/{self.clip_id}/play",
                headers=headers,
                cookies={"x-xsrf-token": self.token},
                proxy=self.proxies,
            )
            print(response.json())


        except Exception as error:
            print(f"Error when sending message: {error}", exc_info=True)

class Poll:
    def __init__(self, username, vote_number):
        self.session = tls_client.Session(client_identifier=f"chrome127", random_tls_extension_order=True, ja3_string=",".join(["771", "-".join([str(random.randint(50, 52392)) for _ in range(15)]), "-".join("45-16-23-65281-35-65037-51-10-43-13-17513-5-0-11-18-27".split("-")), "29-23-24,0"]))
        self.proxy = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\proxy.txt","r").read().splitlines())
        self.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'}
        self.token = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\kick.txt","r").read().splitlines())
        self.username = username
        self.vote_number = vote_number - 1

    def send_vote(self):

        headers = {
            "authority": "kick.com",
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {self.token}",
            "content-type": "application/json",
            "accept-language": "en-US",
            "referer": "https://kick.com/",
            "sec-ch-ua": f'"Chromium";v="127", "Not(A:Brand";v="127", "Google Chrome";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-xsrf-token": self.token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }
        payload = {"id": self.vote_number}
        try:
            response = self.session.post(
                f"https://kick.com/api/v2/channels/{self.username}/polls/vote",
                headers=headers,
                json=payload,
                cookies={"x-xsrf-token": self.token},
                proxy=self.proxies,
            )
            print(response.json())


        except Exception as error:
            print(f"Error when sending message: {error}", exc_info=True)
    


class SingleChat:
    def __init__(self):
        self.session = tls_client.Session(
            client_identifier=f"chrome127", 
            random_tls_extension_order=True, 
            ja3_string=",".join([
                "771", 
                "-".join([str(random.randint(50, 52392)) for _ in range(15)]), 
                "-".join("45-16-23-65281-35-65037-51-10-43-13-17513-5-0-11-18-27".split("-")), 
                "29-23-24,0"
            ])
        )
        self.account_unlocked = False

    def find_token_by_username(self, target_username):
        """Find token for specific username in kick.txt file (not supported, returns None)"""
        # No username in kick.txt, so always return None
        return None

    def unlockAccount(self, channel_username, bot_username, message):
        print(f"Initializing chat as {bot_username}")
        
        # Find token for the specified bot username (not supported, pick random token)
        self.token = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\kick.txt","r").read().splitlines())
        if not self.token:
            print(f"{Fore.RED}[Error] No token found in kick.txt{Fore.RESET}")
            return
            
        self.proxy = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\proxy.txt","r").read().splitlines())
        self.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'}
        self.channel_username = channel_username
        self.message = message

        try:
            headers = {
                "authority": "kick.com",
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US",
                "referer": "https://kick.com/",
                "sec-ch-ua": f'"Chromium";v="127", "Not(A:Brand";v="127", "Google Chrome";v="127"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            }

            response = self.session.get(
                f'https://kick.com/api/v2/channels/{self.channel_username}/chatroom', 
                headers=headers, 
                proxy=self.proxies
            )
            
            if response.status_code != 200:
                print(f"{Fore.RED}[Error] Failed to get chatroom ID: {response.status_code}{Fore.RESET}")
                return
                
            self.chatroom_id = response.json()["id"]
            self.account_unlocked = True
            
            if self.account_unlocked:
                self.send_message()

        except Exception as e:
            print(f"{Fore.RED}[Error] {str(e)}{Fore.RESET}")

    def send_message(self):
        if not self.account_unlocked:
            print(f"{Fore.YELLOW}[Warning] Account not unlocked yet{Fore.RESET}")
            return

        headers = {
            "authority": "kick.com",
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {self.token}",
            "content-type": "application/json",
            "accept-language": "en-US",
            "referer": "https://kick.com/",
            "sec-ch-ua": f'"Chromium";v="127", "Not(A:Brand";v="127", "Google Chrome";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-xsrf-token": self.token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }

        data = {"content": self.message, "type": "message"}
        
        try:
            response = self.session.post(
                f"https://kick.com/api/v2/messages/send/{self.chatroom_id}",
                headers=headers,
                cookies={"x-xsrf-token": self.token},
                json=data,
                proxy=self.proxies,
            )
            
            if response.status_code == 200:
                response_json = response.json()
                if response_json["status"]["error"]:
                    print(f"{Fore.RED}[Error] Message sending error: {response_json['status']['message']}{Fore.RESET}")
                else:
                    print(f"{Fore.GREEN}[Success] Message sent successfully{Fore.RESET}")
            elif response.status_code == 400 and 'FOLLOWERS_ONLY' in response.text:
                print(f"{Fore.YELLOW}[Warning] Followers Mode ONLY{Fore.RESET}")
            elif response.status_code == 400 and 'banned' in response.text:
                print(f"{Fore.RED}[Error] Token is banned{Fore.RESET}")
            elif response.status_code == 403:
                print(f"{Fore.RED}[Error] Cloudflare detected{Fore.RESET}")
            else:
                print(f"{Fore.RED}[Error] Unknown response: {response.status_code} - {response.text}{Fore.RESET}")

        except Exception as error:
            print(f"{Fore.RED}[Error] {str(error)}{Fore.RESET}")
    

