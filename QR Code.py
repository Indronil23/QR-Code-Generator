import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import ImageTk

def generate_qr():
    link = link_entry.get()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=7,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_image = ImageTk.PhotoImage(image=img)
    qr_label.config(image=qr_image)
    qr_label.image = qr_image

def save_qr():
    link = link_entry.get()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=7,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        img.save(save_path)
        messagebox.showinfo("Success", "QR code saved successfully.")

# Create main window
root = tk.Tk()
root.title("QR Code Generator")

# Input field for link
link_label = tk.Label(root, text="Enter Link:", fg="darkblue")
link_label.pack()
link_entry = tk.Entry(root, width=50, bg="lightgray", fg="darkblue", bd=2, relief="solid")
link_entry.pack(pady=5)

# Button to generate QR code
generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr, bg="#4FC7DA", fg="white", bd=2, relief="raised", font=("Helvetica", 12, "bold"))
generate_button.pack(pady=10, ipadx=10, ipady=5)

# Label to display QR code
qr_label = tk.Label(root)
qr_label.pack()

# Button to save QR code
save_button = tk.Button(root, text="Save QR Code", command=save_qr, bg="#2ca02c", fg="white", bd=2, relief="raised", font=("Helvetica", 12, "bold"))
save_button.pack()

root.mainloop()
