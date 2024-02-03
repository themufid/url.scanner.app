import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image, ImageTk

def cek_phishing():
    url = entry_url.get()
    if not is_valid_url(url):
        messagebox.showerror("Error", "URL tidak valid.")
        return
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if 'phishing' in soup.text.lower():
            messagebox.showwarning("Hasil", "URL ini termasuk phishing!")
            log_history(url, "Phishing")
        else:
            messagebox.showinfo("Hasil", "URL ini aman.")
            log_history(url, "Aman")
    except Exception as e:
        messagebox.showinfo("Hasil", "Link Tidak Aman")
        log_history(url, "Tidak Aman")

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
        r'localhost|' 
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def log_history(url, status):
    with open("history.txt", "a") as file:
        file.write(f"URL: {url}, Status: {status}\n")

def show_history():
    with open("history.txt", "r") as file:
        history = file.read()
    messagebox.showinfo("Riwayat Pemeriksaan", history)

def clear_history():
    with open("history.txt", "w") as file:
        file.write("")
    messagebox.showinfo("Riwayat Dihapus", "Riwayat pemeriksaan telah dihapus.")

def edit_link():
    url = entry_url.get()
    new_url = entry_edit.get()
    if is_valid_url(new_url):
        messagebox.showinfo("Edit Berhasil", "Tautan berhasil diubah.")
    else:
        messagebox.showerror("Error", "URL baru tidak valid.")

def download_result():
    with open("history.txt", "r") as file:
        history = file.read()
    with open("hasil_pemeriksaan.txt", "w") as file:
        file.write(history)
    messagebox.showinfo("Hasil Diunduh", "Hasil pemeriksaan telah diunduh sebagai 'hasil_pemeriksaan.txt'.")

root = tk.Tk()
root.title("Phishing URL Scanner")
root.configure(bg='#FFFFFF')
root.geometry("500x520")

canvas = tk.Canvas(root, width=500, height=520, bg='#FFFFFF')
canvas.pack()

image = Image.open("images/heroku.png")
image = image.resize((230, 230), resample=Image.BICUBIC)  
icon = ImageTk.PhotoImage(image)

icon_label = tk.Label(root, image=icon, bg='#FFFFFF')
icon_label.place(relx=0.5, rely=0.2, anchor='center')

app_name_label = tk.Label(root, text="Phishing URL Scanner", bg='#FFFFFF', fg='#333333', font=('Helvetica', 16, 'bold'))
app_name_label.place(relx=0.5, rely=0.32, anchor='center')

app_desc_label = tk.Label(root, text="Aplikasi untuk mendeteksi URL phishing.", bg='#FFFFFF', fg='#333333', font=('Helvetica', 12))
app_desc_label.place(relx=0.5, rely=0.4, anchor='center')

label_url = tk.Label(root, text="Masukkan URL:", bg='#FFFFFF', fg='#333333', font=('Helvetica', 12))
label_url.place(relx=0.5, rely=0.52, anchor='center')

entry_url = tk.Entry(root, width=50)
entry_url.place(relx=0.5, rely=0.56, anchor='center')

button_cek = tk.Button(root, text="Cek", command=cek_phishing, bg='#4CAF50', fg='white', font=('Helvetica', 12))
button_cek.place(relx=0.35, rely=0.66, anchor='center')

button_history = tk.Button(root, text="Lihat Riwayat", command=show_history, bg='#008CBA', fg='white', font=('Helvetica', 12))
button_history.place(relx=0.65, rely=0.66, anchor='center')

button_clear = tk.Button(root, text="Hapus", command=clear_history, bg='#f44336', fg='white', font=('Helvetica', 12))
button_clear.place(relx=0.35, rely=0.77, anchor='center')

button_download = tk.Button(root, text="Unduh Hasil", command=download_result, bg='#795548', fg='white', font=('Helvetica', 12))
button_download.place(relx=0.65, rely=0.77, anchor='center')

footer_frame = tk.Frame(root, bg='#E0E0E0', bd=1, relief=tk.SUNKEN)
footer_frame.place(relx=0, rely=1, relwidth=1, anchor='sw')

footer_label = tk.Label(footer_frame, text="Copyright 2024. Build With ❤️", bg='#E0E0E0', fg='#333333', font=('Helvetica', 10))
footer_label.pack(pady=5)

root.mainloop()
