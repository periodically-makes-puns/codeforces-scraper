import tkinter as tk
from scraper import filter_handle, get_information, get_color, get_rating_data
import matplotlib.pyplot as plt

class CodeforcesScraperFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.namevar = tk.StringVar()
        self.namevar.set("tourist")
        self.username = tk.Entry(self, width=15, textvariable=self.namevar)
        self.username.grid(row=0,column=1)
        tk.Label(self, text="Username: ").grid(row=0, column=0)
        self.submit_button = tk.Button(self, text="Get Info", command=self.get_info)
        self.submit_button.grid(row=0, column=2)
        self.submit_button = tk.Button(self, text="Graph Data", command=self.graph_result)
        self.submit_button.grid(row=0, column=3)
        self.result_box = tk.Text(self, width=50, height=5, state=tk.DISABLED)
        self.result_box.grid(row=1, column=0, columnspan=4)
        self.result_box.tag_config("red", foreground="#ff0000")
        self.result_box.tag_config("violet", foreground="#a0a")
        self.result_box.tag_config("orange", foreground="#ff8c00")
        self.result_box.tag_config("blue", foreground="#0000ff")
        self.result_box.tag_config("cyan", foreground="#03a89e")
        self.result_box.tag_config("green", foreground="#008000")
        self.result_box.tag_config("gray", foreground="#808080")
        self.info = {}
    
    def get_info(self):
        info = get_information(self.namevar.get())
        info["name"] = self.namevar.get()
        rank = info["rank"]
        rating = info["rating"]
        maxRank = info["maxRank"]
        maxRating = info["maxRating"]
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.INSERT, "Name: ")
        self.result_box.insert(tk.INSERT, filter_handle(self.namevar.get()), get_color(rank))
        self.result_box.insert(tk.INSERT, "\nRating: ")
        self.result_box.insert(tk.INSERT, str(rating), get_color(rank))
        self.result_box.insert(tk.INSERT, "\nRank: ")
        self.result_box.insert(tk.INSERT, rank, get_color(rank))
        self.result_box.insert(tk.INSERT, "\nMax Rating: ")
        self.result_box.insert(tk.INSERT, maxRating, get_color(maxRank))
        self.result_box.insert(tk.INSERT, "\nMax Rank: ")
        self.result_box.insert(tk.INSERT, maxRank, get_color(maxRank))
        self.result_box.config(state=tk.DISABLED)
        self.result = info

    def plot_section(self, lb, mb, mini, maxi, color):
        if mini <= lb and maxi >= mb:
            plt.axhspan(lb, mb, facecolor=color, alpha=0.5)
        elif lb <= mini <= mb or lb <= maxi <= mb:
            plt.axhspan(max(mini, lb), min(maxi, mb), facecolor=color, alpha=0.5)

    def mark_bounds(self, mini, maxi):
        self.plot_section(0, 1200, mini, maxi, "#808080")
        self.plot_section(1200, 1400, mini, maxi, "#008000")
        self.plot_section(1400, 1600, mini, maxi, "#03a89e")
        self.plot_section(1600, 1900, mini, maxi, "#0000ff")
        self.plot_section(1900, 2200, mini, maxi, "#a000a0")
        self.plot_section(2200, 2400, mini, maxi, "#ff8c00")
        self.plot_section(2400, 4000, mini, maxi, "#ff0000")

    def graph_result(self):
        name = self.result["name"]
        startTime = self.result["registrationTime"]
        rate_data = get_rating_data(name, startTime)
        fig = plt.figure(figsize=(25, 20))
        ax = fig.add_subplot(111)
        ax.plot(rate_data[0], rate_data[1])
        self.mark_bounds(min(rate_data[1]) - 50, max(rate_data[1]) + 50)
        ax.grid(True, "major", "both", color="#d0b0d0", linewidth=2, linestyle="-")
        ax.grid(True, "minor", "both", color="#a0b0a0", linewidth=1, linestyle="-")
        fig.show()

if __name__ == "__main__":
    root = tk.Tk()
    frame = CodeforcesScraperFrame(root)
    root.mainloop()