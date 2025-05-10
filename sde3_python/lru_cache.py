import requests
import threading
from collections import deque
import time




class Node:
    def __init__(self, key,value):
        self.prev = None
        self.next = None
        self.value = value
        self.key = key

class DLL:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def add(self,key,value):
        node = Node(key,value)

        if self.head is None:
            self.head = node
            self.tail = node
            return node
        node.prev = self.tail
        self.tail.next = node
        self.tail = node

        return node

    
    def remove(self, node):
        key = node.key
        if node.prev is None and node.next is None:
            self.head = self.tail = None
        if node.prev is None:
            self.head = node.next
            if node.next:
                node.next.prev = None
        elif node.next is None:
            self.tail = node.prev
            if self.tail:
                self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        node.next = node.prev = None
        return key

    def __str__(self):
        head = self.tail
        res = []
        while head:
            res.append(str(head.key)+str(head.value))
            head = head.prev
        return "<=>".join(res)

class LRUCache:
    def __init__(self):
        self.cache = {}
        self.length = 4
        self.dll = DLL()
        self.lock = threading.Lock()
    def get(self, key):
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                value = node.value
                key = self.dll.remove(node)
                self.cache[key] = self.dll.add(key, value)
                return value
            return "Key not found"
    
    def put(self, key, value):
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                del_key = self.dll.remove(node)
                del self.cache[del_key]
                self.cache[key] = self.dll.add(key, value)
            elif key not in self.cache:
                if len(self.cache.keys()) < self.length:
                    self.cache[key] = self.dll.add(key, value)
                else:
                    del_key = self.dll.remove(self.dll.head)
                    del self.cache[del_key]
                    self.cache[key] = self.dll.add(key, value)


cache = LRUCache()

urls = deque(["https://www.dummy1.com/",
        "https://www.dummy2.com",
        "https://www.dummy3.com",
        "https://www.dummy4.com", 
        "https://www.dummy2.com", 
        "https://www.dummy1.com"])

urls_lock = threading.Lock()
def worker():
    while True:
        with urls_lock:
            if not urls:
                break
            url = urls.pop()
            try:
                if url in cache.cache:
                    print(cache.cache)
                    print("fetching from cache")
                    return cache.get(url)
                
                response = requests.get(url, timeout=5)
                if url not in cache.cache:
                    cache.put(key=url,value=response.content[:25])
            except Exception as e:
                print(f"error {url}")
            finally:
                print("Complete")
# worker()
threads = []
start = time.time()
for _ in range(3):
        
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)


for i in threads:
    thread.join()
# 0.554011344909668
# worker()
# 2.543705940246582
print(time.time()-start)