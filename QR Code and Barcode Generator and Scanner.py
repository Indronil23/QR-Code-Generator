import cv2
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import ImageTk
import qrcode
import barcode
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
import webbrowser
import threading
import validators  # Library for URL validation


class QRBarcodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR & Barcode Tool")
        self.root.geometry("600x500")

        self.current_image = None
        self.code_label = None  # Define code_label as a class attribute

        self.create_widgets()

    def create_widgets(self):
        # Mode Selection
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=(10, 0))

        tk.Label(mode_frame, text="Select Mode:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=(10, 5))

        self.mode_var = tk.StringVar(value="generator")
        generator_radio = tk.Radiobutton(mode_frame, text="Generator", variable=self.mode_var, value="generator",
                                         command=self.change_mode)
        generator_radio.pack(side=tk.LEFT, padx=5)

        scanner_radio = tk.Radiobutton(mode_frame, text="Scanner", variable=self.mode_var, value="scanner",
                                       command=self.change_mode)
        scanner_radio.pack(side=tk.LEFT, padx=5)

        # Generator Frame
        self.generator_frame = tk.Frame(self.root)

        # Input Field for Link
        link_label = tk.Label(self.generator_frame, text="Enter Link:", font=("Helvetica", 12))
        link_label.pack(pady=(20, 5))

        self.link_entry = tk.Entry(self.generator_frame, width=50)
        self.link_entry.pack(pady=5)

        # Generate Buttons Frame
        generate_buttons_frame = tk.Frame(self.generator_frame)
        generate_buttons_frame.pack(pady=(5, 10))

        # Generate QR Code Button
        generate_qr_button = tk.Button(generate_buttons_frame, text="Generate QR Code", command=self.generate_qr,
                                       bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        generate_qr_button.pack(side=tk.LEFT, padx=5)

        # Generate Barcode Button
        generate_barcode_button = tk.Button(generate_buttons_frame, text="Generate Barcode",
                                            command=self.generate_barcode, bg="#2196F3", fg="white",
                                            font=("Helvetica", 10, "bold"))
        generate_barcode_button.pack(side=tk.LEFT, padx=5)

        # Save Image Button
        save_button = tk.Button(self.generator_frame, text="Save Image", command=self.save_image, bg="#FF9800",
                                fg="white", font=("Helvetica", 10, "bold"))
        save_button.pack(pady=(10, 20))

        # Scanner Frame
        self.scanner_frame = tk.Frame(self.root)

        # Select File Section
        select_file_label = tk.Label(self.scanner_frame, text="Select an image file:", font=("Helvetica", 12))
        select_file_label.pack(pady=(20, 5))

        self.entry = tk.Entry(self.scanner_frame, width=40)
        self.entry.pack(pady=5)

        browse_button = tk.Button(self.scanner_frame, text="Browse", command=self.browse_file)
        browse_button.pack(pady=5)

        # Scan Button
        scan_button = tk.Button(self.scanner_frame, text="Scan", command=self.scan, bg="#FF5722", fg="white",
                                font=("Helvetica", 10, "bold"))
        scan_button.pack(pady=10)

        # Result Display Section
        self.text_box = tk.Text(self.scanner_frame, height=10, wrap=tk.WORD)
        self.text_box.pack(pady=10, padx=10)

        # Loading Animation
        self.loading_label = tk.Label(self.scanner_frame, text="")
        self.loading_label.pack_forget()

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.scanner_frame, orient='horizontal', mode='determinate',
                                            variable=self.progress_var)
        self.progress_bar.pack(pady=5)

        # Initial Mode Setup
        self.change_mode()

        # Create code_label widget and assign it to self.code_label
        self.code_label = tk.Label(self.generator_frame)
        self.code_label.pack()  # Adjust its packing according to your GUI layout

    def change_mode(self):
        mode = self.mode_var.get()
        if mode == "generator":
            self.scanner_frame.pack_forget()
            self.generator_frame.pack(pady=10)
        elif mode == "scanner":
            self.generator_frame.pack_forget()
            self.scanner_frame.pack(pady=10)

    def generate_qr(self):
        link = self.link_entry.get()
        if link:
            if validators.url(link):
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=7,
                    border=4,
                )
                qr.add_data(link)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")
                qr_image = ImageTk.PhotoImage(image=qr_img)
                self.code_label.config(image=qr_image)  # Access code_label using self
                self.code_label.image = qr_image
                self.current_image = qr_img
            else:
                messagebox.showerror("Error", "Please enter a valid URL.")
        else:
            messagebox.showerror("Error", "Please enter a link.")

    def generate_barcode(self):
        link = self.link_entry.get()
        if link:
            if validators.url(link):
                code128 = barcode.get_barcode_class('code128')
                barcode_img = code128(link, writer=ImageWriter()).render()
                barcode_image = ImageTk.PhotoImage(image=barcode_img)
                self.code_label.config(image=barcode_image)  # Access code_label using self
                self.code_label.image = barcode_image
                self.current_image = barcode_img
            else:
                messagebox.showerror("Error", "Please enter a valid URL.")
        else:
            messagebox.showerror("Error", "Please enter a link.")

    def save_image(self):
        if self.current_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            if save_path:
                self.current_image.save(save_path)
                messagebox.showinfo("Success", "Image saved successfully.")
        else:
            messagebox.showerror("Error", "No image to save.")

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.bmp;*.gif")])
        self.entry.delete(0, tk.END)
        self.entry.insert(0, filename)

    def start_loading_animation(self):
        self.loading_label.config(text="Scanning...")
        self.loading_label.pack()
        self.progress_var.set(0)
        self.progress_bar.pack()

    def stop_loading_animation(self):
        self.loading_label.config(text="Scan Complete")
        self.progress_bar.pack_forget()

    def scan(self):
        filepath = self.entry.get()
        if not filepath:
            messagebox.showwarning("Warning", "Please select an image file.")
            return

        self.start_loading_animation()

        threading.Thread(target=self.read_and_display_result, args=(filepath,)).start()

    def read_and_display_result(self, filepath):
        result = None
        try:
            result = self.read_code(filepath)
        except Exception as e:
            messagebox.showerror("Error", str(e))

        if result:
            self.display_result(result)
        else:
            messagebox.showwarning("Scan Result", "No code found.")

        self.stop_loading_animation()

    def read_code(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not open image file '{image_path}'")

        decoded_objects = decode(image)
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        else:
            return None

    def display_result(self, result):
        self.text_box.delete(1.0, tk.END)
        if result.startswith("http://") or result.startswith("https://"):
            self.text_box.insert(tk.END, result, "hyperlink")
            self.text_box.tag_config("hyperlink", foreground="blue", underline=True)
            self.text_box.tag_bind("hyperlink", "<Enter>", lambda event: self.text_box.config(cursor="hand2"))
            self.text_box.tag_bind("hyperlink", "<Leave>", lambda event: self.text_box.config(cursor="arrow"))
            self.text_box.bind("<Button-1>", lambda event: webbrowser.open_new(result))
        else:
            self.text_box.insert(tk.END, result)


if __name__ == "__main__":
    root = tk.Tk()
    app = QRBarcodeApp(root)
    root.mainloop()
