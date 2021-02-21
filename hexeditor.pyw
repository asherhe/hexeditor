# Import Libraries
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from binascii import hexlify, unhexlify
from os import path

# The app
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidgets()

    # Creates all the buttons and stuffz
    def createWidgets(self):
        # Text that bosses you around
        self.selFileText = tk.Label(self)
        self.selFileText.pack()
        self.selFileText.config(text="Enter path of file to be edited in hexadecimal")
        # Choose Filez
        self.inputFrame = tk.Frame(self)
        self.inputFrame.pack()
        self.selectFile = tk.Entry(self.inputFrame)
        self.selectFile.pack(side="left")
        self.Enter = tk.Button(self.inputFrame, text="Enter", command=self.pathEntered)
        self.Enter.pack(side="right")
        # Display contentz
        self.outputBox = tk.Frame(self)
        self.outputBox.pack()
        self.output = ScrolledText(self.outputBox, width=15, height=10)
        self.output.pack(side="left")
        self.save = tk.Button(self.outputBox, text="Save", width=5, height=10, command=self.save)
        self.save.pack(side="right")

    # In a nutshell, converts some text into a buncha hexadecimal bytes
    def hexToString(self, inHex):
        inHex = inHex.decode("utf-8")
        aslist = [(inHex[i:i+2]) for i in range(0, len(inHex), 2)]
        out = ""
        for byte in aslist:
            out += "0x" + byte + "\n"
        return out

    # Someone gave this program a file
    def pathEntered(self):
        # Check if the user is lying about the fileness of the file
        if path.isfile(self.selectFile.get()):
            # User isn't lying about the existence of file: load filez
            f = open(self.selectFile.get(), "rb")
            fileContents = hexlify(f.read())
            fileContents = self.hexToString(fileContents)
            self.output.delete("1.0", tk.END)
            self.output.insert("1.0", fileContents)
        else:
            # User lied: Scream at the user
            self.output.delete("1.0", tk.END)
            self.output.insert("1.0", "Nope, not a file")

    # Halper function
    def remAll(self, l, rem):
        out = []
        for i in l:
            if i == rem:
                pass
            else:
                out.append(i)
        return out

    # Saves the filez
    def save(self):
        # Check if output file is a file
        if path.isfile(self.selectFile.get()):
            # Get the bytes to write
            writeBytes = self.remAll(self.output.get(1.0, tk.END).split("\n"), "")
            # Write the stuffz into the file
            with open(self.selectFile.get(), "wb") as f:
                f.write(unhexlify("".join(format(i[2:], ">02s") for i in writeBytes)))
            # Tell the user that we've saved it, and that they can calm down
            self.save["text"] = "Saved!"
            self.after(1000, self.resetText)
    def resetText(self):
        self.save["text"] = "Save"

# Nothing to do with Tree Roots
root = tk.Tk()
# Set title
root.title("Hexeditor")
# Set icon to this thing that took me two minutes to make
root.iconbitmap("icon.ico")
# NO RESIZING
root.resizable(False, False)
# It's alive!
app = Application(master=root)
app.mainloop()
