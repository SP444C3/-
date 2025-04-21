from tkinter import *
from splitter import Splitter

class Gui:
	def __init__(self):
		self.window = Tk()
		self.moxfield_url = StringVar()
		self.splitter = None

		Label(self.window, text="Moxfield URL:").grid(row=0, columnspan=2)
		Entry(self.window, width=40, textvariable=self.moxfield_url).grid(row=1, columnspan=2)
		Button(self.window, text='Split', width=20, command=self.update).grid(row=2, columnspan=2, padx=10, pady=10)
		Label(self.window, text="Expensive cards to proxy:").grid(row=3, column=0)
		Label(self.window, text="The rest:").grid(row=3, column=1)

		self.proxy_list = Text(self.window, width=30)
		self.proxy_list.grid(row=4, column=0)
		self.og_list = Text(self.window, width=30)
		self.og_list.grid(row=4, column=1)

		self.window.mainloop()

	def update(self):
		if self.splitter is None:
			self.splitter = Splitter(self.moxfield_url.get())
		else:
			self.splitter.set_url(self.moxfield_url.get())

		self.proxy_list.delete("1.0", END)
		self.og_list.delete("1.0", END)

		proxies = self.splitter.get_proxy_list()
		ogs = self.splitter.get_og_list()

		for card in proxies:
			self.proxy_list.insert(END, f"{card['quantity']} {card['name']}\n")

		for card in ogs:
			self.og_list.insert(END, f"{card['quantity']} {card['name']}\n")
