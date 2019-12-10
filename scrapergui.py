import tkinter as tk
from scraper import get_information, get_color

class CodeforcesScraperFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        