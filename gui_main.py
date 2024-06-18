import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import psutil
from en_decrypt import decrypt_file_with_rsa, encrypt_file_with_rsa

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Projekt z BSK")
        self.center_window(500, 500)
        self.create_main_menu()
        self.check_usb()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def create_main_menu(self):
        self.clear_window()
        self.create_label("Wybierz opcję", font=("Helvetica", 16), pady=20)

        self.create_button("Szyfrowanie pliku", self.encrypt_file_menu)
        self.create_button("Odszyfrowanie pliku", self.decrypt_file_menu)
        self.create_button("Podpisywanie dokumentu", self.sign_document_menu)
        self.create_button("Weryfikacja dokumentu", self.verify_document_menu)

        self.usb_status_frame = tk.Frame(self.root)
        self.usb_status_frame.pack(pady=10)
        self.usb_status_label = tk.Label(self.usb_status_frame, text="Sprawdzanie stanu USB...")
        self.usb_status_label.pack(side=tk.LEFT)
        self.update_usb_status()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_button(self, text, command):
        tk.Button(self.root, text=text, command=command, width=30, height=2).pack(pady=10)

    def create_label(self, text, **kwargs):
        label = tk.Label(self.root, text=text, **kwargs)
        label.pack(pady=5)
        return label

    def update_label(self, label, text):
        label.config(text=text if text else "Nie wybrano pliku")

    def file_dialog(self, label, file_type, initialdir=None):
        file_path = filedialog.askopenfilename(title=f"Wybierz {file_type}", initialdir=initialdir)
        self.update_label(label, file_path)
        return file_path

    def select_file(self, file_type, label_attr, file_attr):
        if file_type == "klucz prywatny" and self.usb_drive_path is None:
            messagebox.showerror("Błąd", "Nie wykryto podłączonego pendrive'a.")
            return
        file_path = self.file_dialog(getattr(self, label_attr), file_type, self.usb_drive_path if file_type == "klucz prywatny" else None)
        setattr(self, file_attr, file_path)

    def encrypt_file_menu(self):
        self.clear_window()
        self.create_label("Szyfrowanie pliku", font=("Helvetica", 16), pady=20)

        self.create_button("Wybierz plik", lambda: self.select_file("plik do zaszyfrowania", "input_file_label", "input_file_path"))
        self.input_file_label = self.create_label("Nie wybrano pliku")

        self.create_button("Wybierz klucz publiczny", lambda: self.select_file("klucz publiczny", "public_key_label", "public_key_path"))
        self.public_key_label = self.create_label("Nie wybrano klucza publicznego")

        self.create_button("Szyfruj", self.encrypt_file)
        self.create_button("Powrót", self.create_main_menu)

    def encrypt_file(self):
        if not hasattr(self, 'input_file_path') or not self.input_file_path:
            messagebox.showerror("Błąd", "Nie wybrano pliku do zaszyfrowania")
            return

        if not hasattr(self, 'public_key_path') or not self.public_key_path:
            messagebox.showerror("Błąd", "Nie wybrano pliku z kluczem publicznym")
            return

        try:
            encrypt_file_with_rsa(self.input_file_path, self.public_key_path)
            messagebox.showinfo("Sukces", "Plik został zaszyfrowany pomyślnie.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas szyfrowania pliku: {str(e)}")

    def decrypt_file_menu(self):
        self.clear_window()
        self.create_label("Odszyfrowanie pliku", font=("Helvetica", 16), pady=20)

        self.create_button("Wybierz plik", lambda: self.select_file("plik do odszyfrowania", "encrypted_file_label", "encrypted_file_path"))
        self.encrypted_file_label = self.create_label("Nie wybrano pliku")

        self.create_button("Wybierz klucz prywatny", lambda: self.select_file("klucz prywatny", "private_key_label", "private_key_path"))
        self.private_key_label = self.create_label("Nie wybrano klucza prywatnego")

        self.create_button("Odszyfruj", self.decrypt_file)
        self.create_button("Powrót", self.create_main_menu)

    def decrypt_file(self):
        if not hasattr(self, 'encrypted_file_path') or not self.encrypted_file_path:
            messagebox.showerror("Błąd", "Nie wybrano pliku do odszyfrowania")
            return

        if not hasattr(self, 'private_key_path') or not self.private_key_path:
            messagebox.showerror("Błąd", "Nie wybrano pliku z kluczem prywatnym")
            return

        pin = simpledialog.askstring("PIN", "Wprowadź PIN do klucza prywatnego:", show='*')
        if not pin:
            return

        try:
            decrypt_file_with_rsa(self.encrypted_file_path, self.private_key_path, pin)
            messagebox.showinfo("Sukces", "Plik został odszyfrowany pomyślnie.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas odszyfrowania pliku: {str(e)}")

    def sign_document_menu(self):
        self.clear_window()
        self.create_label("Podpisywanie dokumentu", font=("Helvetica", 16), pady=20)

        self.create_button("Wybierz plik do podpisania", lambda: self.select_file("plik do podpisania", "sign_file_label", "sign_file_path"))
        self.sign_file_label = self.create_label("Nie wybrano pliku")

        self.create_button("Wybierz klucz prywatny", lambda: self.select_file("klucz prywatny", "private_key_label", "private_key_path"))
        self.private_key_label = self.create_label("Nie wybrano klucza prywatnego")

        self.create_button("Podpisz", self.sign_document)
        self.create_button("Powrót", self.create_main_menu)

    def sign_document(self):
        if not hasattr(self, 'sign_file_path') or not self.sign_file_path:
            messagebox.showerror("Błąd", "Nie wybrano pliku do podpisania")
            return

        if not hasattr(self, 'private_key_path') or not self.private_key_path:
            messagebox.showerror("Błąd", "Nie wybrano klucza prywatnego do podpisu")
            return

        pin = simpledialog.askstring("PIN", "Wprowadź PIN do klucza prywatnego:", show='*')
        if not pin:
            return

        try:
            sign_file(self.sign_file_path, pin, self.private_key_path)
            messagebox.showinfo("Sukces", "Dokument został podpisany pomyślnie.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas podpisywania dokumentu: {str(e)}")

    def verify_document_menu(self):
        self.clear_window()
        self.create_label("Weryfikacja dokumentu", font=("Helvetica", 16), pady=20)

        self.create_button("Wybierz podpisany plik", lambda: self.select_file("podpisany plik", "signed_file_label", "signed_file_path"))
        self.signed_file_label = self.create_label("Nie wybrano podpisanego pliku")

        self.create_button("Wybierz plik z podpisem", lambda: self.select_file("plik z podpisem", "signature_file_label", "signature_file_path"))
        self.signature_file_label = self.create_label("Nie wybrano pliku z podpisem")

        self.create_button("Wybierz klucz publiczny", lambda: self.select_file("klucz publiczny", "public_key_label", "public_key_path"))
        self.public_key_label = self.create_label("Nie wybrano klucza publicznego")

        self.create_button("Weryfikuj", self.verify_document)
        self.create_button("Powrót", self.create_main_menu)

    def verify_document(self):
        if not hasattr(self, 'signed_file_path') or not self.signed_file_path:
            messagebox.showerror("Błąd", "Nie wybrano podpisanego pliku do weryfikacji")
            return

        if not hasattr(self, 'public_key_path') or not self.public_key_path:
            messagebox.showerror("Błąd", "Nie wybrano klucza publicznego do weryfikacji")
            return

        if not hasattr(self, 'signature_file_path') or not self.signature_file_path:
            messagebox.showerror("Błąd", "Nie wybrano pliku z podpisem")
            return

        try:
            verify_file(self.signed_file_path, self.public_key_path, self.signature_file_path)
            messagebox.showinfo("Sukces", "Podpis dokumentu został zweryfikowany poprawnie.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas weryfikacji dokumentu: {str(e)}")

    def check_usb(self):
        usb_devices = [device.device for device in psutil.disk_partitions() if 'removable' in device.opts]
        if usb_devices:
            usb_status_text = "Podłączony pendrive"
            usb_status_color = "green"
            self.usb_drive_path = usb_devices[0]
        else:
            usb_status_text = "Brak podłączonego pendrive'a"
            usb_status_color = "red"
            self.usb_drive_path = None

        if hasattr(self, 'usb_status_label') and self.usb_status_label.winfo_exists():
            self.usb_status_label.config(text=usb_status_text, fg=usb_status_color)

    def update_usb_status(self):
        self.check_usb()
        self.root.after(1000, self.update_usb_status)

def sign_file(private_key_path, pin, file_path):
    # Tutaj zaimplementuj logikę podpisywania
    pass

def verify_file(public_key_path, file_path, file_sig_path):
    # Tutaj zaimplementuj logikę weryfikacji
    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
