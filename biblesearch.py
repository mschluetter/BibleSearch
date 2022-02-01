from typing import List
import requests
from bs4 import BeautifulSoup
from configparser import ConfigParser

class BibleVerse():
	version: str #Bibleversion
	chapter: str #Book and Chapter
	versenumber: List #List of Versenumbers
	verse: str #Value of vers(es)
	location: str #Location in bible

	def __init__(self, verse: str, version: str = "LUT"):
		self.version = version
		
		if verse == "":
			self.versenumber = []
			self.verse = "-- NOCH NICHT BEKANNT --"
			self.location = "OFFEN"

		else:
			self.versenumber =[v.strip() for v in verse.split(",")]
			self.versenumber[1] = self.Get_Versenumbers(self.versenumber[1])
			self.verse = self.Get_Verse()
			self.location = self.Get_Location()

	def Get_Location(self) -> str:
		if len(self.versenumber[1]) > 1:
			return f"{self.versenumber[0]}, {self.versenumber[1][0]}-{self.versenumber[1][-1]}"
		return f"{self.versenumber[0]}, {self.versenumber[1][0]}"

	def Get_Versenumbers(self, numbers: str) -> List:
		def Find_Delimiter(text):
			for t in text:
				try: int(t)
				except: return t
		return numbers.split(Find_Delimiter(numbers))

	def Get_Verse(self) -> str:
		r = requests.get("https://www.bibleserver.com/"+self.version+"/"+self.versenumber[0])
		#print(r.status_code)
		if r.status_code != 200:
			return "Vers existiert nicht, Kapitel existiert nicht..."
		soup = BeautifulSoup(r.text, 'html.parser')

		spans = soup.find_all("span", class_="verse-content--hover")
		verse = ""

		if len(self.versenumber[1]) == 1:
			try:
				verse = spans[int(self.versenumber[1][0])-1].text
			except: verse = "Vers existiert nicht!"
		else:
			try:
				for n in range(int(self.versenumber[1][0]), int(self.versenumber[1][1])+1):
					verse = verse + " " + spans[int(n)-1].text
			except: verse = "Verse existieren nicht!"

		h1 = soup.find_all("h1")
		if len(h1) == 1:
			self.versenumber[0] = h1[0].text.strip()
			if "." in self.versenumber[0]: self.versenumber[0] = self.versenumber[0].replace(".", ". ")

		return verse

	def __repr__(self) -> str:
		return f"{self.location}: {self.verse}"

def main():
	#Load Config.ini
	config = ConfigParser()
	config.read("config.ini")
	#print(config['BibleSearch']['bibleVersion'])

	#Ask for verse
	verse = input("Bitte Vers eingeben [Format: 1. Johannes 3, 2-4]: ")
	
	#Create Bibleverse Object
	bibleverse = BibleVerse(verse, config['BibleSearch']['bibleVersion'])
	print(bibleverse.location)

if __name__ == "__main__":
	main()