import tkinter as tk
from tkinter import filedialog, messagebox
from huffman import HuffmanCoding
import os

class HuffmanUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compressor")
        self.root.geometry("600x300")
        
        # File selection
        self.file_label = tk.Label(root, text="Select a file:", font=("Arial", 12))
        self.file_label.pack(pady=10)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(root, textvariable=self.file_path_var, width=60)
        self.file_entry.pack(pady=5)
        
        self.browse_btn = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_btn.pack(pady=5)
        
        # Compress button
        self.compress_btn = tk.Button(root, text="Compress File", command=self.compress_file, width=20, bg="lightgreen")
        self.compress_btn.pack(pady=10)
        
        # Decompress button
        self.decompress_btn = tk.Button(root, text="Decompress File", command=self.decompress_file, width=20, bg="lightblue")
        self.decompress_btn.pack(pady=10)
        
        # Result label
        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=20)
    
    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.file_path_var.set(filename)
    
    def compress_file(self):
        path = self.file_path_var.get()
        if not os.path.exists(path):
            messagebox.showerror("Error", "File does not exist")
            return
        
        h = HuffmanCoding()
        try:
            output_path = h.compress_file(path)
            original_size = os.path.getsize(path)
            compressed_size = os.path.getsize(output_path)
            ratio = compressed_size / original_size
            self.result_label.config(
                text=f"Compressed!\nOutput: {output_path}\nOriginal: {original_size} bytes\nCompressed: {compressed_size} bytes\nRatio: {ratio:.2f}x"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def decompress_file(self):
        path = self.file_path_var.get()
        if not os.path.exists(path):
            messagebox.showerror("Error", "File does not exist")
            return
        
        h = HuffmanCoding()
        try:
            output_path = h.decompress_file(path)
            self.result_label.config(
                text=f"Decompressed!\nOutput: {output_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanUI(root)
    root.mainloop()
