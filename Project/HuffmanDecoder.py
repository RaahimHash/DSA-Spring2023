from tkinter import *
from tkinter import filedialog

def decode(encoded: bytes, mapping: dict):

    def refine_data(encoded: bytes): # necessary since we added extra bits in bits_to_bytes() that aren't part of the actual code

        compressedbits = ""
        # converting the encoded text into bits
        for byteindex in range(len(encoded)):
            compressedbits += bin(encoded[byteindex])[2:].zfill(8) # converting the bytes to bits, removing the first 2 indices which are just a default prefix "0b" and zfill-ing to ensure the length is 8

        compressedbits = compressedbits[:-8-int(compressedbits[-8:], 2)] # removing the extra bits added through bits_to_bytes()

        return compressedbits

    encoded = refine_data(encoded)
    decoded = ""
    current = ""
    reverse_mapping = {mapping[char]: char for char in mapping} # reversing the mapping making the codes as keys so we can access them in O(1) time when decoding

    for bit in encoded:

        current += bit 

        if current in reverse_mapping:
            decoded += reverse_mapping[current]
            current = "" # resetting current once we've decoded a character

    return decoded


def process_input():

    main = Tk()

    def open1():
        global file1
        file1 = filedialog.askopenfilename(title = "Choose a file", filetypes = (('text files', '*.txt'),('All files', '*.*')))
        if file1:
            file1 = file1[file1.rfind("/")+1:]
            filelabel1.config(text = file1)
        
    def open2():
        global file2
        file2 = filedialog.askopenfilename(title = "Choose a file", filetypes = (('text files', '*.txt'),('All files', '*.*')))
        if file2:
            file2 = file2[file2.rfind("/")+1:]
            filelabel2.config(text = file2)

    def close():
        main.destroy()

    main.title("Upload files")
    main.geometry("300x300")
    main.resizable(False, False)
    label = Label(main, text="Select the file you wish to decode").pack(pady = 10)
    filelabel1 = Label(main, text=f"Selected: None")
    filelabel1.pack()
    button1 = Button(main, text = "Choose file", command = open1).pack(pady = 5)
    label = Label(main, text="Select the file's mapping").pack(pady = 10)
    filelabel2 = Label(main, text=f"Selected: None")
    filelabel2.pack()
    button2 = Button(main, text = "Choose file", command = open2).pack(pady = 5)
    button3 = Button(main, text = "Decode", command = close).pack(pady = 25)

    main.mainloop()
    
    try:
        filename = file1
        mapping = file2

        with open(filename, "rb") as f:  # reading compressed file (in bytes)
            compressedtext = f.read()

        with open(mapping, "r", encoding = "utf8") as f:  # reading and storing the mapping for decoding
            mapping = eval(f.read())

        decoded = decode(compressedtext, mapping) # calls decode() passing the encoded text and the mapping as parameters

        with open(f"decoded_{filename}", "w", encoding = "utf8") as f:
            f.write(decoded)

        success = Tk()

        def more():
            global file1, file2
            success.destroy()
            file1 = None
            file2 = None
            process_input()

        def quit():
            success.destroy()

        success.title("Decoding successful!")
        success.geometry("700x100")
        success.resizable(False, False)
        label = Label(success, text="Decoding successful!\nWould you like to decode more files or close the decoder?").pack(pady = 10)
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
        label = Label(fail, text="There was an error in the decoding. Please ensure you selected the correct files.").pack(pady = 10)
        button = Button(fail, text = "Try again", command = tryagain).pack(pady = 5)

        fail.mainloop()

process_input()
