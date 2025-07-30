import httpx, json, time, threading, random, string, m3u8, traceback, requests, uuid, irc ;from websocket import create_connection ;from colorama import Fore
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import os
import sys


class Tools:
    def bordcast_id(self, user):

        headers = {'Connection': 'keep-alive','Pragma': 'no-cache','Cache-Control': 'no-cache','sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"','Accept-Language': 'en-US','sec-ch-ua-mobile': '?0','Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36','Content-Type': 'text/plain;charset=UTF-8','Client-Session-Id': '51789c1a5bf92c65','Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko','X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr','sec-ch-ua-platform': '"Windows"','Accept': '*/*','Origin': 'https://www.twitch.tv','Sec-Fetch-Site': 'same-site','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Referer': 'https://www.twitch.tv/',}
        data = '''{
        "operationName":"WatchTrackQuery",
        "variables":{
            "channelLogin":"'''+user+'''",
            "videoID":null,
            "hasVideoID":false
        },
        "extensions":{
            "persistedQuery":{
                "version":1,
                "sha256Hash":"d8e507b720dd231780d57d325fb3a9bb8ee1ee60d424ae106e6dab328ea9b4c6"
            }
        }
        }'''

        try:
            response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
            return response.json()['data']['user']['lastBroadcast']['id']
        except:
            return False
    def user_id(self, user):
        headers = {'Connection': 'keep-alive','Pragma': 'no-cache','Cache-Control': 'no-cache','sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"','Accept-Language': 'en-US','sec-ch-ua-mobile': '?0','Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36','Content-Type': 'text/plain;charset=UTF-8','Client-Session-Id': '51789c1a5bf92c65','Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko','X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr','sec-ch-ua-platform': '"Windows"','Accept': '*/*','Origin': 'https://www.twitch.tv','Sec-Fetch-Site': 'same-site','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Referer': 'https://www.twitch.tv/',}
        data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
        try:
            response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
            return response.json()[0]['data']['user']['id']
        except:
            return False
    def check_chat(self, target:str):
        self.proxy = random.choice(open('C:\\Users\\Administrator\\Desktop\\private bot system\\data\\proxies.txt', 'r').read().splitlines())
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'es-ES',
            'Cache-Control': 'no-cache',
            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
            'Connection': 'keep-alive',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': 'https://www.twitch.tv',
            'Referer': 'https://www.twitch.tv/',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2; like Mac OS X) AppleWebKit/602.49 (KHTML, like Gecko)  Chrome/52.0.2707.177 Mobile Safari/533.5',
        }

        data = '[{"operationName": "ChatRoomState","variables": {"login": "' + target + '"},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "04cc4f104a120ea0d9f9d69be8791233f2188adf944406783f0c3a3e71aff8d2"}}}, {"operationName": "Chat_ChannelData","variables": {"channelLogin": "' + target + '"},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "3c445f9a8315fa164f2d3fb12c2f932754c2f2c129f952605b9ec6cf026dd362"}}}, {"operationName": "UseLive","extensions": {"persistedQuery": {"sha256Hash": "639d5f11bfb8bf3053b424d9ef650d04c4ebb7d94711d644afb08fe9a0fad5d9","version": 1} },"variables": {"channelLogin": "' + target + '"}}]'
        response = requests.post('https://gql.twitch.tv/gql', headers=headers, data=data, proxies={'http': f'http://{self.proxy}', 'http': f'http://{self.proxy}'})
        emote = response.json()[0]['data']['channel']['chatSettings']['isEmoteOnlyModeEnabled']
        follow_only = response.json()[0]['data']['channel']['chatSettings']['followersOnlyDurationMinutes']
        email_verify = response.json()[0]['data']['channel']['chatSettings']['accountVerificationOptions']['emailVerificationMode']
        phone_verify = response.json()[0]['data']['channel']['chatSettings']['accountVerificationOptions']['phoneVerificationMode']
        rules = len(response.json()[1]['data']['channel']['chatSettings']['rules'])
        streaming = response.json()[2]['data']['user']['stream']
        try:
            sub_mode = response.json()[0]['data']['channel']['subscriptionProducts'][0]['hasSubOnlyChat']
        except:
            sub_mode = False
        return emote, follow_only, email_verify, phone_verify, rules, streaming, sub_mode

    def get_follower_count(self, user):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
            'Content-Type': 'application/json',
            'Origin': 'https://www.twitch.tv',
            'Referer': 'https://www.twitch.tv/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        query = '''{ user(login: "%s") { followers { totalCount } } }''' % user
        try:
            response = requests.post('https://gql.twitch.tv/gql', headers=headers, json={'query': query})
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and data['data']['user'] is not None:
                    return data['data']['user']['followers']['totalCount']
                else:
                    return 0
            else:
                return 0
        except Exception as e:
            return str(e)

    def get_profile(self, user):
        try:
            query = """
            {
              user(login: "%s") {
                id
                displayName
                profileImageURL(width: 300)
                description
                followers {
                  totalCount
                }
              }
            }
            """ % user
            headers = {
                "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
                "Content-Type": "application/json"
            }
            response = requests.post("https://gql.twitch.tv/gql", headers=headers, json={"query": query})
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and data['data']['user'] is not None:
                    profile_pic = data['data']['user']['profileImageURL']
                    return profile_pic
                else:
                    return "https://static-cdn.jtvnw.net/user-default-pictures-uv/294c98b5-e34d-42cd-a8f0-140b72fba9b0-profile_image-300x300.png"
            else:
                return "https://static-cdn.jtvnw.net/user-default-pictures-uv/294c98b5-e34d-42cd-a8f0-140b72fba9b0-profile_image-300x300.png"
        except Exception as e:
            return "https://static-cdn.jtvnw.net/user-default-pictures-uv/294c98b5-e34d-42cd-a8f0-140b72fba9b0-profile_image-300x300.png"


class DaTa:
    
    followed_tokens = {}
    invalid_token = []

class FollowProgress:
    def __init__(self, total):
        self.total = total
        self.done = 0
        self.success = 0
        self.failed = 0
        self.lock = threading.Lock()
        self.finished = False

class Follow:
    
    def __init__(self):
        self.followed_tokens = {}
        self.invalid_token = []
        # Connection pool for better performance
        self.session_pool = {}
        self.session_lock = threading.Lock()
        # Token cache to reduce file I/O
        self.token_cache = []
        self.token_cache_lock = threading.Lock()
        self.cache_loaded = False

    def get_follow_count_for_target(self, target_id):
        count = 0
        for token, followed_targets in DaTa.followed_tokens.items():
            if target_id in followed_targets:
                count += 1
        return count
    
    def load_tokens_cache(self):
        """Load tokens into memory cache to reduce file I/O"""
        if not self.cache_loaded:
            with self.token_cache_lock:
                if not self.cache_loaded:
                    token_file = "C:\\Users\\Administrator\\Desktop\\private bot system\\data\\tokens_with_proxies.txt"
                    try:
                        with open(token_file, "r") as f:
                            self.token_cache = f.read().splitlines()
                        self.cache_loaded = True
                    except Exception as e:
                        print(f"[ ERROR ] Failed to load token cache: {e}")
                        return []
        return self.token_cache

    def get_session(self, proxy):
        """Get or create a session for a specific proxy to enable connection pooling"""
        with self.session_lock:
            if proxy not in self.session_pool:
                proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"}
                self.session_pool[proxy] = httpx.Client(
                    proxies=proxies,
                    timeout=40,
                    limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
                )
            return self.session_pool[proxy]

    def select_valid_tokens(self, target_id, tokens_data, count):
        """Efficiently select a valid token without excessive loops"""
        valid_tokens = []
        
        # Pre-filter valid tokens
        for token_line in tokens_data:
            try:
                token_id, token, proxy = token_line.split("|")
                
                # Skip invalid tokens
                if token in DaTa.invalid_token:
                    continue
                    
                # Check if token hasn't been used for this target
                if token not in DaTa.followed_tokens or target_id not in DaTa.followed_tokens[token]:
                    valid_tokens.append((token_id, token, proxy))
            except Exception:
                continue
        
        random.shuffle(valid_tokens)
        return valid_tokens[:count]

    def send_follow(self, target_id, follow_count, progress=None, username=None, real_gained=0, max_retries=10):
        # Check follower count before
        follower_count_before = None
        follower_count_after = None
        if username and real_gained == 0:
            try:
                follower_count_before = Tools().get_follower_count(username)
                print(f"[INFO] Follower count before: {follower_count_before}")
            except Exception as e:
                print(f"[WARN] Could not get follower count before: {e}")
        else:
            follower_count_before = None
        tokens_data = self.load_tokens_cache()
        if not tokens_data:
            print("[ ERROR ] No tokens available")
            if progress:
                with progress.lock:
                    progress.finished = True
            return 0
        total_success = 0
        attempted_tokens = set()
        attempts = 0
        while total_success < follow_count and attempts < max_retries:
            needed = follow_count - total_success
            valid_tokens = self.select_valid_tokens(target_id, tokens_data, needed)
            if not valid_tokens:
                print("[ ERROR ] No more valid tokens for this target")
                break
            def follow_worker(token_data):
                token_id, token, proxy = token_data
                payload = json.dumps([{
                    "operationName": "FollowUserMutation",
                    "variables": {
                        "targetId": str(target_id),
                        "disableNotifications": False
                    },
                    "extensions": {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "cd112d9483ede85fa0da514a5657141c24396efbc7bac0ea3623e839206573b8"
                        }
                    }
                }])
                headers = {
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "pl-PL",
                    "Authorization": "OAuth " + token,
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Host": "gql.twitch.tv",
                }
                session = self.get_session(proxy)
                try:
                    res = session.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                    if "FORBIDDEN" in res.text or "Unauthorized" in res.text:
                        with self.token_cache_lock:
                            if token not in DaTa.invalid_token:
                                DaTa.invalid_token.append(token)
                        success = False
                    elif "failed integrity check" in res.text:
                        success = False
                    else:
                        if token not in DaTa.followed_tokens:
                            DaTa.followed_tokens[token] = []
                        DaTa.followed_tokens[token].append(target_id)
                        success = True
                    if progress:
                        with progress.lock:
                            progress.done += 1
                            if success:
                                progress.success += 1
                            else:
                                progress.failed += 1
                    return success
                except Exception as e:
                    if progress:
                        with progress.lock:
                            progress.done += 1
                            progress.failed += 1
                    return False
            with ThreadPoolExecutor(max_workers=min(50, len(valid_tokens))) as executor:
                results = list(executor.map(follow_worker, valid_tokens))
            successes = sum(results)
            total_success += successes
            for token_data in valid_tokens:
                attempted_tokens.add(token_data[1])
            tokens_data = [line for line in tokens_data if line.split("|")[1] not in attempted_tokens]
            attempts += 1
        # Check follower count after
        real_gained_now = 0
        if username:
            try:
                follower_count_after = Tools().get_follower_count(username)
                print(f"[INFO] Follower count after: {follower_count_after}")
                if isinstance(follower_count_before, int) and isinstance(follower_count_after, int):
                    real_gained_now = follower_count_after - follower_count_before
                    print(f"[RESULT] Real followers gained: {real_gained_now} / {follow_count} ({(real_gained_now/follow_count)*100:.1f}% success rate)")
            except Exception as e:
                print(f"[WARN] Could not get follower count after: {e}")
        return real_gained_now

    def get_real_gained(self, username, before):
        try:
            after = Tools().get_follower_count(username)
            if isinstance(before, int) and isinstance(after, int):
                return after - before
        except Exception:
            pass
        return 0




class Reaction:
    def __init__(self,):
        self.reacted_tokens = {}
    def send_reactions(self, target_id, react_count, react_type, bordcast_id, tokens_data):
        class Threads():
                tha = 0
        def send_reaction(i):
            data = None
            for i in range(len(tokens_data)):
                data = json.loads(random.choice(tokens_data))
                token = data['access']
                if not token in self.reacted_tokens:
                    break
                elif not target_id in self.reacted_tokens[token]:
                    break
                else:
                    data = None                     ########################
            Threads.tha = Threads.tha + 1           #   MADE BY TWIDDLLO   #
            try:                                    ########################
                try:
                    data = json.loads(self.integrity_list[i])
                except:
                    return
                Authorization = data['access']
                Integrity = data['integrity']['token']
                proxy = "http://" + data['integrity']['proxy']
                X_Device_Id = data['integrity']['data']['X-Device-ID']
                Client_Id = data['integrity']['data']['Client-ID']
                User_Agent = data['integrity']['data']['User-Agent']
                payload = '[{"operationName":"UpdateViewerStreamFeedback","variables":{"input":{"broadcastID":"'+bordcast_id+'","viewerID":"'+target_id+'","channelID":"'+target_id+'","feedback":["'+react_type+'"]}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"4fa64766ea733d828b864ce0c582e672e4a313126addc5c338a69d0916609566"}}}]'
                headers = {
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Authorization': 'OAuth '+Authorization,
                    'Client-Id': Client_Id,
                    'Client-Integrity': Integrity,
                    'User-Agent': User_Agent,
                    'X-Device-Id': X_Device_Id,
                    }
                res = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers,proxies=proxy,timeout=40)
                print(res.json)
                try:
                    res.json()[0]['data']['updateViewerStreamFeedback']['__typename']
                except:
                    print("rid")
            except:
                print("rid")
        def start():
            for i in range(react_count):
                while True:
                    time.sleep(0.01)
                    if Threads.tha < 20:
                        threading.Thread(
                            target=send_reaction, args=(i,)).start()
                        break
                    else:
                        time.sleep(1)
        threading.Thread(target=start).start()



#follow

class Chat:

    def __init__(self) -> None:
        self.reacted_tokens = {}
        self.chat_message_str = '@client-nonce=<RANDOM_ID> PRIVMSG #<CHAT_NAME> :<MESSAGE>'
        self.socket_mess_list = ['CAP REQ :twitch.tv/tags twitch.tv/commands','PASS oauth:<TOKEN>','NICK <TOKEN_NICk>','USER <TOKEN_NICk> 8 * :<TOKEN_NICk>', 'JOIN #<CHAT_NAME>', self.chat_message_str]

    def prase(self,x,target:str,username:str, message:str, token:str):
        return x.replace("<TOKEN>",token).replace("<RANDOM_ID>", str(uuid.uuid4().hex)).replace("<CHAT_NAME>",target).replace("<TOKEN_NICk>",username).replace("<MESSAGE>",message)
    

    def send_messages(self, target, message, message_count, chat: bool, delay):
        self.message_initial = message
        self.message = message
        self.delay = delay
        self.words = []
        if self.message_initial:
            if "pastebin.com" in self.message_initial:
                prefix = self.message_initial[:self.message_initial.find(".com")+5]
                sufix = self.message_initial[self.message_initial.find(".com")+5:]
                link = prefix + "raw/" + sufix
                r = requests.get(link)
                for line in r.text.splitlines():
                    self.words.append(line.strip())
                self.message = self.words

        class Threads():
            tha = 0
        def send_message(i):
            Threads.tha = Threads.tha + 1
            data = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\chattokens.txt", 'r').read().splitlines())
            token = data.split(":")[1]
            username = data.split(":")[3]
            proxy = random.choice(open(r"C:\Users\Administrator\Desktop\private bot system\data\proxy.txt", 'r').read().splitlines())
            try:
                headers = {
                    'connection':'Upgrade',
                    'host':'irc-ws.chat.twitch.tv',
                    'sec-websocket-version':'13',
                    'upgrade':'websocket'
                }

                ws = None

                if "@" in proxy:
                    ip = proxy.split("@")[1].split(":")[0]
                    port = proxy.split("@")[1].split(":")[1]
                    passw = proxy.split("@")[0].split(":")[1]
                    login = proxy.split("@")[0].split(":")[0]

                    ws = create_connection("wss://irc-ws.chat.twitch.tv/", extra_headers=headers,
                                        http_proxy_host=ip,http_proxy_port=int(port) , http_proxy_auth=(login, passw))
                else:
                    ip = proxy.split(":")[0]
                    port = proxy.split(":")[1]
                    ws = create_connection("wss://irc-ws.chat.twitch.tv/", extra_headers=headers,
                                        http_proxy_host=ip,http_proxy_port=int(port))
                    
                if len(self.words) != 0:
                        self.message = random.choice(self.words)
                for x in self.socket_mess_list:
                    mess = self.prase(x,target,username,self.message,token)
                    ws.send(mess)
                print(self.prase(f'{self.chat_message_str}', target, username, self.message, token)) 
                ws.send(self.prase(f'{self.chat_message_str}', target, username, self.message, token)) 
                ws.close()
            except Exception as e:
                print(e)
            Threads.tha = Threads.tha - 1
        def start():
            for i in range(message_count):
                while True:
                    if not self.message_initial:
                        self.message = random.choice(open(r'C:\Users\Administrator\Desktop\private bot system\data\messages.txt', 'r', encoding='utf-8').read().splitlines())
                    time.sleep(0.01) if chat else time.sleep(self.delay)
                    if Threads.tha < 20:
                        threading.Thread(target=send_message, args=(i,)).start()
                        break
                    else:
                        time.sleep(1)

        threading.Thread(target=start).start()









# chat
# class chat:

#     def __init__(self,):
#         self.followed_tokens = {}

#     def send_follow(self, target_id, follow_count, tokens_data):

#         class Threads():
#             tha = 0
#             followed = 0
        
#         def follow(i):
#             Threads.tha = Threads.tha + 1
            
#             if Threads.followed >= follow_count: return
            
#             try:
#                 token = None; proxy = None

#                 for i in range(len(tokens_data)):
#                     try:
#                         token_id, token, token_username, email, e_code, proxy = random.choice(tokens_data).split("|")

#                         if not token in self.followed_tokens:
#                             break
#                         elif not target_id in self.followed_tokens[token]:
#                             break
#                         else:
#                             token = None
#                     except:
#                         pass
#                 if token == None:
#                     return


#                 payload = json.dumps([
#                     {
#                         "operationName": "FollowUserMutation",
#                         "variables": {
#                         "targetId": str(target_id),
#                         "disableNotifications": False
#                         },
#                         "extensions": {
#                         "persistedQuery": {
#                             "version": 1,
#                             "sha256Hash": "cd112d9483ede85fa0da514a5657141c24396efbc7bac0ea3623e839206573b8"
#                         }
#                         }
#                     }
#                     ])
                
#                 headers = {
#                     "Api-Consumer-Type": "mobile; Android/1500000",
#                     "Authorization": "OAuth " + token,
#                     "Client-ID": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp",
#                     "Connection": "Keep-Alive",
#                     "Content-Type": "application/json",
#                     "Host": "gql.twitch.tv",
#                     "Transfer-Encoding": "chunked",
#                     "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M) tv.twitch.android.app/15.0.0/1500000",
#                     "X-APOLLO-OPERATION-NAME": "FollowUserMutation",
#                     "X-App-Version": "15.0.0",
#                 }
              
#                 res = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers, proxies="http://"+proxy, timeout=40)
#                 # response_data = json.loads(res.text)
#                 # for item in response_data:
#                 #     if item["data"]["followUser"]["error"] is None:
#                 #         print(f"[ {Fore.GREEN}V{Fore.RESET} ] Success")




#                 if False:
#                     print(f"[ {Fore.RED}V{Fore.RESET} ] Success")
                    
#                 elif "FORBIDDEN" in res.text:
#                     print(f"[ {Fore.RED}X{Fore.RESET} ] token DIED ", token)
#                 elif "SERVER OFFLINE" in res.text:
#                     print(f"[ {Fore.RED}X{Fore.RESET} ] server offline ")
#                 elif "failed integrity check" in res.text:
#                     print(f"[ {Fore.RED}X{Fore.RESET} ] INTEGRITY DIED ", token)
#                 elif "Unauthorized" in res.text:
#                     print(f"[ {Fore.RED}X{Fore.RESET} ] Token is fully dead ", token)
#                 else:
#                     print(f"[ {Fore.GREEN}V{Fore.RESET} ] Success")
                
                
                
#                 Threads.followed = Threads.followed + 1
                
#                 if not token in self.followed_tokens:
#                     self.followed_tokens[token] = []
#                 self.followed_tokens[token].append(target_id)
                

                
#             except:
#                 return

#             Threads.tha = Threads.tha - 1

#         def start():
            
#             count = None
#             if len(tokens_data) < follow_count:
#                 count = len(tokens_data)
#             else:
#                 count = follow_count
            
#             for i in range(count):
#                 while True:
#                     if Threads.followed >= count: return
#                     time.sleep(0.01)
#                     if Threads.tha < 20:
#                         threading.Thread(
#                             target=follow, args=(i,)).start()
#                         break
#                     else:
#                         time.sleep(1)

#         threading.Thread(target=start).start()
#chat




class Followw:

    integrity_errors = 0
    print("uwu")

    def __init__(self):
        self.followed_tokens = {}

    def send_follow(self, target_id, follow_count, tokens_file):
        class Threads:
            tha = 0

        def read_tokens():
            with open(tokens_file, 'r') as file:
                tokens_data = file.readlines()
            return tokens_data

        def write_tokens(tokens_data):
            with open(tokens_file, 'w') as file:
                file.writelines(tokens_data)

        def follow():
            
            Threads.tha += 1
            try:
                data = None
                tokens_data = read_tokens()

                for _ in range(len(tokens_data)):
                    token_str = random.choice(tokens_data)
                    data = json.loads(token_str)
                    token = data['access']

                    if token not in self.followed_tokens:
                        break
                    elif target_id not in self.followed_tokens[token]:
                        break
                    else:
                        data = None

                if data is None:
                    return

                # Remove the used token from the list and write back to file
                tokens_data.remove(token_str)
                write_tokens(tokens_data)

                Authorization = data['access']
                Integrity = data['integrity']['token']
                proxy = "http://" + data['integrity']['proxy']
                X_Device_Id = data['integrity']['data']['X-Device-ID']
                Client_Id = data['integrity']['data']['Client-ID']
                User_Agent = data['integrity']['data']['User-Agent']

                payload = '[{"operationName":"FollowButton_FollowUser","variables":{"input":{"disableNotifications":false,"targetID":"'+str(target_id)+'"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"800e7346bdf7e5278a3c1d3f21b2b56e2639928f86815677a7126b093b2fdd08"}}}]'
                headers = {
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Authorization': 'OAuth '+Authorization,
                    'Client-Id': Client_Id,
                    'Client-Integrity': Integrity,
                    'User-Agent': User_Agent,
                    'X-Device-Id': X_Device_Id,
                }
                try:
                    res = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers, proxies=proxy, timeout=40)
                    response_text = res.text

                    if str(target_id) in response_text:
                        print(f" [ + ] Success ")
                    elif "FORBIDDEN" in response_text:
                        print(f" [ERROR] TOKEN DIED {Authorization}")
                    elif "failed integrity check" in response_text:
                        print(f" [ERROR] INTEGRITY DIED {Authorization}")
                        Followw().integrity_errors = Followw().integrity_errors + 1
                    else:
                        print(f" [ - ] Error \n{res.text}")
                
                except Exception as e:
                    print(f"exception: {e}")
            except Exception as e:
                print(f"Exception: {str(e)}")

            Threads.tha = Threads.tha - 1
        
        def start():
            for _ in range(follow_count + Followw().integrity_errors):
                while True:
                    time.sleep(0.01)
                    if Threads.tha < 20:
                        threading.Thread(target=follow).start()
                        break
                    else:
                        time.sleep(1)

        threading.Thread(target=start).start()











#timers[idd].start


  
  
class Send:
    def __init__(self) -> None:
        UserAgents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.0.0.0 Safari/{1}.36'.format(
                str(random.randint(95,116)), str(random.randint(10,999))
            ),
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{0}.0) Gecko/{1} Firefox/{0}.0'.format(
                str(random.randint(95,107)), str(random.randint(10100101,30100101))
            ),
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.0.0.0 Safari/{1}.36 Edg/{0}.0.1462.42'.format(
                str(random.randint(95,116)), str(random.randint(1,99999))
            ),
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.0.0.0 Safari/537.36 OPR/{0}.0.0.0'.format(
                str(random.randint(95,116))
            )
        ]
        self.UserAgent = random.choice(UserAgents)

    def send(self, proxy, arg, token, ultra, tm, timer):
        try:
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US',
                'Authorization': 'undefined',
                'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                'Connection': 'keep-alive',
                'Content-Type': 'text/plain; charset=UTF-8',
                'Device-ID': ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(32)),
                'Origin': 'https://www.twitch.tv',
                'Referer': 'https://www.twitch.tv/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': self.UserAgent,
            }
            if token is not None:
                jd = json.loads(token)
                headers['Authorization'] = "OAuth " + jd['access']
                headers['Device-ID'] = jd['integrity']['data']['X-Device-ID']

            data = '{"operationName":"PlaybackAccessToken_Template","query":"query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, params: {platform: \\"web\\", playerBackend: \\"mediaplayer\\", playerType: $playerType}) @include(if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken(id: $vodID, params: {platform: \\"web\\", playerBackend: \\"mediaplayer\\", playerType: $playerType}) @include(if: $isVod) {    value    signature    __typename  }}","variables":{"isLive":true,"login":"'+arg+'","isVod":false,"vodID":"","playerType":"site"}}'

            proxies = {
                "http": proxy,
                "https": proxy
            }

            response = None
            if ultra:
                response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data, timeout=100, verify=False)
            else:
                response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data, proxies=proxies, timeout=1000, verify=False)

            response.raise_for_status()  # Raise HTTPError for bad responses
            if "Unauthorized" in response.text:
                print("Error: Unauthorized access")
                return False

            response_json = response.json()
            signature = response_json['data']['streamPlaybackAccessToken']['signature']
            value = response_json['data']['streamPlaybackAccessToken']['value']
            
            headers = {
                'Accept': 'application/x-mpegURL, application/vnd.apple.mpegurl, application/json, text/plain',
                'Referer': '',
                'User-Agent': self.UserAgent,
            }

            params = {
                'acmb': 'e30=',
                'allow_source': 'true',
                'fast_bread': 'true',
                'p': '7914395',
                'play_session_id': ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(32)),
                'player_backend': 'mediaplayer',
                'playlist_include_framerate': 'true',
                'reassignments_supported': 'true',
                'sig': signature,
                'supported_codecs': 'avc1',
                'token': value,
                'transcode_mode': 'vbr_v2',
                'cdm': 'wv',
                'player_version': '1.22.0',
            }

            if ultra:
                response = httpx.get(f'https://usher.ttvnw.net/api/channel/hls/{arg}.m3u8', params=params, headers=headers, timeout=100, verify=False)
            else:
                response = httpx.get(f'https://usher.ttvnw.net/api/channel/hls/{arg}.m3u8', params=params, headers=headers, proxies=proxies, timeout=1000, verify=False)

            response.raise_for_status()  # Raise HTTPError for bad responses
            m3u8_obj = m3u8.loads(response.text)
            lowest_quality = m3u8_obj.playlists[-1]
            lowest_quality_url = lowest_quality.uri

            view_loop = 0

            while int(time.time() - timer) < tm:
                res = httpx.get(lowest_quality_url, headers=headers, proxies=proxies, timeout=40, verify=False)
                res.raise_for_status()  # Raise HTTPError for bad responses
                lowest_quality_m3u8 = m3u8.loads(res.text)

                if ultra:
                    return

                for segment in lowest_quality_m3u8.segments:
                    if int(time.time() - timer) > tm:
                        return

                    headers = {
                        'Referer': '',
                        'User-Agent': self.UserAgent,
                    }
                    segment_url = segment.uri
                    res = httpx.get(segment_url, headers=headers, proxies=proxies, timeout=40, verify=False)
                    res.raise_for_status()  # Raise HTTPError for bad responses
                    view_loop += 1
                    if res.status_code == 200:
                        print("Segment downloaded successfully")
                    else:
                        print(f"Segment download failed with status code {res.status_code}")
                        print("Response text:", res.text)
                        time.sleep(segment.duration)
        except httpx.HTTPStatusError as e:
            print(f"HTTP Status Error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Request Error: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

class Data():
    x = 0

class CommandTimer:
    def __init__(self):
        self.start = int(time.time())

    def restart(self):
        self.start = int(time.time())

timers = {}

class Send_V:
    def send_views(self, target_name, threads_count, tm, idd):
        timers[idd] = CommandTimer()

        def spamview(proxy, token):
            while int(time.time()) - timers[idd].start < tm:
                try:
                    res = Send().send(proxy, target_name, token, False, tm, timers[idd].start)
                    if res is False:
                        token = None
                except Exception as e:
                    print(f"Error in spamview: {e}")
        
        tokens_view_data = []
        try:
            with open("C:\\Users\\Administrator\\Desktop\\private bot system\\integrity.txt", "r") as file:
                tokens = file.read().splitlines()
            for _ in range(threads_count):
                dt = random.choice(tokens)
                while dt in tokens_view_data:
                    dt = random.choice(tokens)
                tokens_view_data.append(dt)
        except FileNotFoundError:
            print("Error: integrity.txt file not found")
            return
        except Exception as e:
            print(f"Error reading tokens: {e}")
            return
        
        try:
            with open("C:\\Users\\Administrator\\Desktop\\private bot system\\data\\proxy.txt", 'r') as file:
                proxies = file.read().splitlines()
        except FileNotFoundError:
            print("Error: proxy.txt file not found")
            return
        except Exception as e:
            print(f"Error reading proxies: {e}")
            return
        
        for i in range(threads_count):
            try:
                token = tokens_view_data[i]
            except IndexError:
                print("Error: Not enough tokens provided for the number of threads")
                token = None
            
            proxy = random.choice(proxies)
            threading.Thread(target=spamview, args=("http://" + proxy, token)).start()
        
        timers[idd].restart()