# Date 2025-05-05
# Decorators and context managers
# questions to be updated

# Date 2025-05-06
# linked list using __iter__ and __next__
# class Node:
#     def __init__(self, val):
#         self.val = val
#         self.next = None

# class LinkedListIterator:

#     def __init__(self, head):
#         self.head = head

#     def __next__(self):
#         if self.head is not None:
#             val = self.head.val
#             self.head = self.head.next
#             return val
#         else:
#             raise StopIteration

# class LinkedList:
#     def __init__(self):
#         self.length = 0
#         self.head = None
    
#     def __iter__(self):
#         return LinkedListIterator(self.head)
    
#     def insert(self, inp_list):
#         self.head = Node(inp_list[0])
#         self.length += 1
#         node = self.head
#         for i in inp_list[1:]:
#             self.length += 1
#             node.next = Node(i)
#             node = node.next
   


# ll = LinkedList()
# ll.insert([1,2,3,4])

# _t = iter(ll)
# print(f"t{ _t.__next__()}")
# _x = iter(ll)
# print(next(_x))
# print(f"t{next(_t)}")

# print(next(_x))
# print(f"t{next(_t)}")

# print(next(_x))
# print(f"t{next(_t)}")

# # late binding and closure
# import threading
# import time

# def schedule_tasks():
#     for i in range(5):
#         t = threading.Timer(1, lambda i=i: print(f"Running task {i}"))
#         t.start()

# schedule_tasks()
# time.sleep(2)  # wait for threads to finish

# Date 2025-05-07
# strategy and observer pattern

# from abc import ABC, abstractmethod

# # Abstract base class
# class ChannelABC(ABC):
#     @abstractmethod
#     def update(self, data):
#         pass

# # Concrete channel implementations
# class Email(ChannelABC):
#     def update(self, data):
#         print(f"Sending Email: {data}")

# class SMS(ChannelABC):
#     def update(self, data):
#         print(f"Sending SMS: {data}")

# class PushNotification(ChannelABC):
#     def update(self, data):
#         print(f"Sending Push: {data}")

# # Notification Manager
# class Notification:
#     def notify(self, channel_list):
#         data = "New system event"
#         for channel in channel_list:
#             channel.update(data)

# # Usage
# notification = Notification()
# channels = [Email(), SMS(), PushNotification()]
# notification.notify(channels)


# Date 2025-05-07
# Date 2025-05-08
# Date 2025-05-09
# LRU cache with threading
# on a highter level this is like a focus group for people who 
# are preparing for interviews the website wants to track data
# of the most commong websites visited for there prep and create analysis so that others can follow the path
# so it collects a basic five websites on initial login and keeps track of how long they spend on each of them per day
# so throughout the day we need to keep tracking the number of times the website was visited
# if a new website was visited and the user wants the app to track then it will added
# as soon as the user logs in the webistes will be cached and number will be increased to track the umber of hours spent
# instead of having this each tiem we can cache and keep incremting the number thats where our lrucache comes into play

#basic implementation of the above


# class Node:
#     def __init__(self, key, value):
#         self.prev = None
#         self.next = None
#         self.key = key
#         self.value = value

# class DLL:

#     def __init__(self):
#         self.head = self.tail = Node(0,0)
        
    
#     def add(self, key, value):
#         node = Node(key,value)
#         node.prev = self.tail
#         self.tail.next = node
#         self.tail = node
#         return node
    
#     def remove(self,value=None):
#         print(">>>>>>>>>>>here")
#         if value is None:
#             next_node = self.head.next.next
#         #     next_node.next.prev = self.head
#             self.head.next = next_node
#             return
        
#         remove_node = value
#         print(">>>>>>>>>>>here")
#         remove_node.prev.next = remove_node.next
#         remove_node.next.prev = remove_node
#         return



# class LRUCache:
#     def __init__(self, length):
#         self.cache = {}
#         self.length = length or 10
#         self.dll = DLL()
    
#     def add(self,key,value):
#         if len(self.cache) < self.length:
#             if key not in self.cache:
#                 self.cache[key] = self.dll.add(key, value)
#                 self.length += 1
#         else:
#             self.remove()
#             self.dll.add(value)
    
#     def get(self,key):
        
#         if key in self.cache:
#             value = self.cache[key]
#             print("<<<<<<<<<<<<<<<<<<")
#             self.remove(value)
#             self.cache[key] = self.dll.add(key,value)
#             print(self.cache[key])
#             return self.cache[key].value
    
#     def remove(self, key=None):
#         if key is None:
#             key = self.dll.head.key
#         self.dll.remove(key)
#         del self.cache[key]

# cache = LRUCache(3)
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

urls = deque(["https://www.udemy.com/",
        "https://www.google.com",
        "https://www.linkedin.com",
        "https://www.bytebytego.com", 
        "https://www.bytebytego.com", 
        "https://www.neetcode.com"])

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