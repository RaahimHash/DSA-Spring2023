from tkinter import *
from tkinter import filedialog

class Node:
    def __init__(self, char: str | None, freq: int, left: dict | None = None, right: dict | None = None): 
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right


class MinHeap: # priority queue based on ascending order of frequency
    def __init__(self, arr : list):
        self.heap = arr.copy()
        for index in range(len(self.heap)-1,-1,-1):
            self.siftdown(index)

    def siftup(self, index : int):
        parent = (index-1)//2 # index of parent node
        while index != 0 and self.heap[index].freq < self.heap[parent].freq:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index-1)//2

    def siftdown(self, index : int):
        left = 2*index + 1 # index of left child
        right = 2*index + 2 # index of right child
        while (left < len(self.heap) and self.heap[index].freq > self.heap[left].freq) or (right < len(self.heap) and self.heap[index].freq > self.heap[right].freq):
            smallest = left if (right >= len(self.heap) or self.heap[left].freq < self.heap[right].freq) else right
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest
            left = 2*index + 1
            right = 2*index + 2

    def extract_min(self):
        minval = self.heap[0]
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        self.heap.pop()
        self.siftdown(0)
        return minval
    
    def insert(self, element):
        self.heap.append(element)
        self.siftup(len(self.heap)-1)


def build_tree(text: str):

    frequencies = {} 

    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1 # storing frequencies of characters

    node_list = [Node(char, frequencies[char]) for char in frequencies] # list of leaf nodes for each char and frequency
    pq = MinHeap(node_list)

    while len(pq.heap) > 1: # runs until only one element left, which would be the entire tree
        left : Node = pq.extract_min() # taking out two smallest frequency nodes
        right : Node = pq.extract_min()
        root = Node(None, left.freq+right.freq, left, right) # connecting them to a root whose frequency is their sum

        pq.insert(root)

    return pq.extract_min() # return the tree


def build_mapping(root: Node):

    def huffmantree_dfs(root: Node, code: str, mapping: dict):

        if root.char: # only possible at a leaf node
            mapping[root.char] = code # assigning the code to that character

        else:
            code += "0"
            huffmantree_dfs(root.left, code, mapping) # adding 0 to code and traversing the left side
            code = code[:-1] + "1" 
            huffmantree_dfs(root.right, code, mapping) # removing the added 0, adding 1 to code and traversing the right side

    if root.char:  # only possible if there is only one character, otherwise root["char"] is always None
        return {root.char: "0"}

    mapping = {}

    huffmantree_dfs(root, "", mapping)

    return mapping


def encode(text: str):

    def bits_to_bytes(data: str): # necessary to write the data into a file as we cannot write in bits

        data += (8-len(data) % 8)*"0" + bin(8-len(data) % 8)[2:].zfill(8) # making the length of data a multiple of 8 and also concatenating the byte representation of the number of zeroes added to achieve this so we can remove them later on in the decode() function

        b = []

        for i in range(0, len(data), 8):
            b.append(int(data[i:i+8], 2)) # grabbing 8 bits and converting them to binary number system

        return bytes(b) # bytes() converts any iterable to an immutable object consisting of bytes

    tree = build_tree(text)
    mapping = build_mapping(tree)

    encoded = ""

    for char in text:
        encoded += mapping[char] # iterating over the text and converting each character to its code in bits

    encoded = bits_to_bytes(encoded) # converting the bits into bytes

    return (encoded, mapping) # returning both the text and mapping to use for decoding


def process_input():

    main = Tk()

    def open1():
        global file1
        file1 = filedialog.askopenfilename(title = "Choose a file", filetypes = (('text files', '*.txt'),('All files', '*.*')))
        if file1:
            file1 = file1[file1.rfind("/")+1:]
            filelabel1.config(text = file1)

    def close():
        main.destroy()

    main.title("Upload file")
    main.geometry("300x200")
    main.resizable(False, False)
    label = Label(main, text="Select the file you wish to encode").pack(pady = 10)
    filelabel1 = Label(main, text=f"Selected: None")
    filelabel1.pack()
    button1 = Button(main, text = "Choose file", command = open1).pack(pady = 5)
    button3 = Button(main, text = "Encode", command = close).pack(pady = 25)

    main.mainloop()

    try:
        filename = file1

        with open(filename, "r", encoding="utf8") as f:  # opening file to read text data
            text = f.read()

        encoded = encode(text)

        with open(f"compressed_{filename}", "wb") as f:  # writing the encoded text to a file (in bytes)
            f.write(encoded[0])

        with open(f"mapping_{filename}", "w", encoding="utf8") as f:  # storing the mapping in a file
            f.write(str(encoded[1]))

        success = Tk()

        def more():
            global file1
            success.destroy()
            file1 = None
            process_input()

        def quit():
            success.destroy()

        success.title("Encoding successful!")
        success.geometry("700x100")
        success.resizable(False, False)
        label = Label(success, text="Encoding successful!\nWould you like to encode more files or close the encoder?").pack(pady = 10)
        button = Button(success, text = "Continue", command = more).place(x = 250, y = 50)
        button = Button(success, text = "Close", command = quit).place(x = 400, y = 50)

        success.mainloop()

    except:
        fail = Tk()

        def tryagain():
            fail.destroy()
            process_input()

        fail.title("ERROR")
        fail.geometry("700x100")
        fail.resizable(False, False)
        label = Label(fail, text="There was an error in the encoding.").pack(pady = 10)
        button = Button(fail, text = "Try again", command = tryagain).pack(pady = 5)

        fail.mainloop()

process_input()
