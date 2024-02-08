import tkinter as tk
from tkinter import ttk

# Ana pencereyi oluştur
root = tk.Tk()
root.title("PowerStat V4")
root.geometry("800x600")


# Ana bölüm çerçevesi
main_frame = tk.Frame(root, bd=1, relief=tk.SOLID)
main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Hardware Diagnostic çerçevesi
frame1 = tk.LabelFrame(main_frame, text="Hardware Diagnostic", height=100)
frame1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Hardware Detail çerçevesi
frame2 = tk.LabelFrame(main_frame, text="Hardware Detail", height=100)
frame2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# Battery çerçevesi
frame3 = tk.LabelFrame(main_frame, text="Battery", height=100)
frame3.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

# Ana çerçevenin sütunlarını eşit genişlikte yapılandır
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)



root.mainloop()
