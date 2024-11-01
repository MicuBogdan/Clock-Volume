import tkinter as tk
from tkinter import ttk
import time
import ctypes
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Inițializarea interfeței de volum folosind pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

class TransparentClockApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Elimină bara de sus
        self.root.geometry("300x150")
        self.root.attributes('-transparentcolor', "gray")  # Face fundalul transparent

        # Setează fundalul fereastrei ca fiind "gray" pentru transparență completă
        self.root.config(bg="gray")

        # Stil pentru a face fundalul slider-ului transparent și butonul negru
        style = ttk.Style()
        style.configure("TScale",
                        background="gray",  # Fundalul slider-ului, care devine transparent
                        troughcolor="gray",  # Face canalul slider-ului complet transparent
                        sliderrelief="flat",  # Fără relief pentru un aspect minimalist
                        sliderthickness=10)  # Grosimea butonului de tragere

        # Label pentru a afișa ora curentă
        self.time_label = tk.Label(root, font=("Helvetica", 24), fg="black", bg="gray")
        self.time_label.pack(pady=10)

        # Slider pentru controlul volumului
        self.volume_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=self.set_volume, style="TScale")
        self.volume_slider.set(self.get_current_volume())
        self.volume_slider.pack(pady=10)

        # Eveniment pentru a preveni mutarea ferestrei când se folosește slider-ul
        self.volume_slider.bind("<Button-1>", self.start_adjusting)
        self.volume_slider.bind("<ButtonRelease-1>", self.stop_adjusting)

        # Actualizarea orei
        self.update_time()

        # Evenimente pentru a permite mutarea ferestrei cu mouse-ul
        self.root.bind("<Button-1>", self.start_move)   # Detectează începutul mutării
        self.root.bind("<B1-Motion>", self.do_move)     # Detectează mișcarea cu mouse-ul
        self.root.bind("<ButtonRelease-1>", self.stop_move)  # Oprește mutarea

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Actualizare la fiecare secundă

    def set_volume(self, value):
        volume_level = float(value) / 100  # Conversia valorii slider-ului la intervalul [0.0, 1.0]
        volume.SetMasterVolumeLevelScalar(volume_level, None)

    def get_current_volume(self):
        # Obține volumul curent și îl transformă într-un interval de la 0 la 100
        return int(volume.GetMasterVolumeLevelScalar() * 100)

    def start_adjusting(self, event):
        self.adjusting_volume = True  # Indică faptul că se ajustează volumul

    def stop_adjusting(self, event):
        self.adjusting_volume = False  # Indică faptul că ajustarea volumului s-a terminat

    def start_move(self, event):
        if not hasattr(self, 'adjusting_volume') or not self.adjusting_volume:
            self._x = event.x
            self._y = event.y

    def do_move(self, event):
        if not hasattr(self, 'adjusting_volume') or not self.adjusting_volume:
            x = self.root.winfo_pointerx() - self._x
            y = self.root.winfo_pointery() - self._y
            self.root.geometry(f"+{x}+{y}")

    def stop_move(self, event):
        self._x = None
        self._y = None

# Inițializare fereastră principală
root = tk.Tk()
app = TransparentClockApp(root)
root.mainloop()
