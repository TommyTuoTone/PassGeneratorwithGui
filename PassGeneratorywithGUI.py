# __________                          ________                                   __
# \______   \_____    ______ ______  /  _____/  ____   ____   ________________ _/  |_  ___________
#  |     ___/\__  \  /  ___//  ___/ /   \  ____/ __ \ /    \_/ __ \_  __ \__  \\   __\/  _ \_  __ \
#  |    |     / __ \_\___ \ \___ \  \    \_\  \  ___/|   |  \  ___/|  | \// __ \|  | (  <_> )  | \/
#  |____|    (____  /____  >____  >  \______  /\___  >___|  /\___  >__|  (____  /__|  \____/|__|
# PassGenerator   \/  By:\/Tom R\/          \/     \/     \/     \/           \/
import tkinter as tk
import os
import secrets
import string
import time
class PassGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('PassGenerator')
        self.root.geometry('215x308+850+275')
        root.resizable(False, False)
        icon_filename = 'ICON.ico'
        icon_path = os.path.join(os.path.dirname(__file__), icon_filename)
        self.root.iconbitmap(icon_path)
        self.setup_ui()
        root.config(bg='#202124')
    def setup_ui(self):
        self.setup_frame_1()
    def setup_frame_1(self):
        self.frame_1 = tk.LabelFrame(self.root, font=('Arial', 18), bg='#202124', borderwidth=1, relief='flat')
        self.frame_1.pack(padx=0, pady=0, anchor='center')
        tk.Label(self.frame_1, text="PassGenerator", font=('Arial', 18, 'bold'), fg='#F4DFC8', bg='#202124').pack(padx=0, pady=0, anchor='center')
        tk.Label(self.frame_1, text="By: Tom R.", font=('Arial', 15, 'bold'), fg='#F4DFC8', bg='#202124').pack(padx=0, pady=0, anchor='center')
        tk.Label(self.frame_1, text="Password Length:", font=('Arial', 14, 'bold'), fg='#F4DFC8', bg='#202124').pack(padx=0, pady=0, anchor='center')
        self.spinbox = tk.Spinbox(self.frame_1, font=('Arial', 10, 'bold'), readonlybackground= '#F4DFC8', cursor='arrow', from_=8, to=100, state='readonly', width=6,)
        self.spinbox.pack(padx=0, pady=0, anchor='center')
        tk.Button(self.frame_1, text="Generate Password", width=15, font=('Arial', 16, 'bold'), bg="#F4DFC8", fg='#202124', activebackground='#202124', activeforeground='#F4DFC8', border= 0,
            command=self.generate_and_populate).pack(padx=0, pady=5, anchor='center')
        self.textbox = tk.Text(self.frame_1, height=5, width=22, font=('Arial', 12, 'bold',), bg='#F4DFC8', cursor='arrow', state='disabled', borderwidth=1, relief='flat', border= 0)
        self.textbox.pack(padx=0, pady=0, anchor='center')
        tk.Button(self.frame_1, text="Copy to Clipboard", width=15, font=('Arial', 16, 'bold'), bg='#F4DFC8', fg='#202124', activebackground='#202124', activeforeground='#F4DFC8', border= 0,
            command=self.copy_to_clipboard).pack(padx=0, pady=5, anchor='center')
        self.spinbox.bind("<MouseWheel>", self.on_spinbox_scroll)
    def generate_secrets_password(self, length):
        if length < 8:
            raise ValueError("Password length must be at least 8")
        characters = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = [
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.digits),
                secrets.choice(string.punctuation),
            ]
            password.extend(secrets.choice(characters) for _ in range(length - 4))
            secrets.SystemRandom().shuffle(password)  # Using SystemRandom, not module random, to shuffle secrets password
            password = ''.join(password)
            if (
                any(c in string.ascii_lowercase for c in password) and
                any(c in string.ascii_uppercase for c in password) and
                any(c in string.digits for c in password) and
                any(c in string.punctuation for c in password)):
                return password
    def generate_and_populate(self):
        password_length = int(self.spinbox.get())
        if password_length < 8 or password_length > 100:
            generated_password = 'Invalid length. Please choose a length between 8 and 100.'
            textbox_bg = '#202124'
            textbox_fg = 'red'
        else:
            generated_password = self.generate_secrets_password(password_length)
            textbox_bg = '#F4DFC8'
            textbox_fg = '#202124'
        self.textbox.configure(state='normal', bg=textbox_bg, fg=textbox_fg)
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert('1.0', generated_password)
        self.textbox.tag_configure('invalid', foreground='red' if 'Invalid' in generated_password else 'black')
        self.textbox.configure(state='disabled')
        self.flash_textbox(times=1, delay=0.1)
    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.textbox.get('1.0', 'end-1c'))
        self.root.update()
        self.flash_textbox(times=2, delay=0.1)  # Adjust the number of times and delay as needed
    def flash_textbox(self, times=2, delay=0.1):
        for i in range(times):
            self.textbox.configure(bg='#202124', fg='#F4DFC8')
            self.root.update()
            time.sleep(delay)
            self.textbox.configure(bg='#F4DFC8', fg='#202124')
            self.root.update()
            time.sleep(delay)
    def on_spinbox_scroll(self, event):
        if event.delta > 0:
            self.spinbox.invoke('buttonup')
        else:
            self.spinbox.invoke('buttondown')
if __name__ == '__main__':
    root = tk.Tk()
    app = PassGeneratorApp(root)
    root.mainloop()