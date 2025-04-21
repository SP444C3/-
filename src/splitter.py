import re
import json
import cloudscraper

class Splitter:
	def __init__(self, url):
		self.deck_id = None
		self.scraper = cloudscraper.create_scraper()
		self.set_url(url)
		self.MAX_CARD_PRICE = 5.0
		self.proxy_list = None
		self.og_list = None

	def set_url(self, url):
		self.url = url
		self.deck_id = None

		if not self.validate_url():
			raise ValueError("Invalid Moxfield URL")
		else:
			self.deck_id = self.url.split("/")[-1]

	def validate_url(self):
		pattern = r'^https?://moxfield\.com/decks/[A-Za-z0-9_\-]+$'
		if re.match(pattern, self.url) is not None:
			return True
		else:
			return False
	
	def get_deck_data(self):

		api_url = f"https://api2.moxfield.com/v2/decks/all/{self.deck_id}"

		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
			"Content-Type": "text/html; charset=utf-8",
		}
		response = self.scraper.get(api_url, headers=headers)

		if response.status_code != 200:
			raise Exception(f"Failed to fetch deck data: {response.status_code} - {response.text}")
		
		response = response.json()

		cards = response["mainboard"]
		cards.update(response["commanders"])

		self.set_card_list(cards)
		
	
	def set_card_list(self, cards):
		self.cards = cards
		self.proxy_list = []
		self.og_list = []

		for name, item in self.cards.items():
			card = {
				"name": name,
				"price": item["card"]["prices"].get("eur", item["card"]["prices"].get("usd", 0) * 0.9),
				"quantity": item["quantity"]
			}

			if card["price"] > self.MAX_CARD_PRICE:
				self.proxy_list.append(card)
			else:
				self.og_list.append(card)

	def get_proxy_list(self):
		if self.proxy_list is None:
			self.get_deck_data()
		
		return self.proxy_list
	
	def get_og_list(self):
		if self.og_list is None:
			self.get_deck_data()
		
		return self.og_list
