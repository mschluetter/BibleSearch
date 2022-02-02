from typing import List
import requests
from bs4 import BeautifulSoup

class BibleSearch:
	""" Connects to bibleserver and returns the verse and location """
	version: str #Bibleversion
	chapter: str #Book and Chapter
	versenumber: List[int] #List of versenumbers
	verse: str #Value of vers(es)
	location: str #Location in bible
	initsetter: bool #Checks if there is a Set of verse at creation

	def __init__(self, verse:str="NO", version:str="LUT") -> None:
		self.version = version
		if verse != "NO":
			self.initsetter = True
			self.Set_Verse(verse)
		else: self.initsetter = False

	def Set_Verse(self, verse:str="") -> None:
		while True:
			if not self.initsetter:
				verse = input("Bitte Bibelstelle eingeben [Format: 1. Johannes 3, 2-4]: ")
			else:
				self.initsetter = False

			if verse == "":
				self.chapter = ""
				self.verse = "-- NOCH NICHT BEKANNT --"
				self.location = "OFFEN"
				break

			else:
				if not "," in verse:
					print("Falsches Format!")
					self.verse = "NO"
					continue
				
				self.chapter = verse.split(",")[0].strip()
				self.versenumber = self.Get_Versenumbers(verse.split(",")[1].strip())

				if not self.chapter or not self.versenumber:
					print("Falsches Format!")
					self.verse = "NO"
					continue
				
				valid, self.verse = self.Get_Verse()
				if valid:
					if len(self.versenumber) > 1:
						self.location = f"{self.chapter}, {self.versenumber[0]}-{self.versenumber[1]}"
					else: self.location = f"{self.chapter}, {self.versenumber[0]}"
					break
				else: 
					print(self.verse)
					self.verse = "NO"
					continue

	def Get_Versenumbers(self, numbers: str) -> List:
		""" Find the Delimiter and return the Versenumbers as List"""
		def Find_Delimiter(text):
			for t in text:
				try: int(t)
				except: return t
		return numbers.split(Find_Delimiter(numbers))

	def Get_Verse(self) -> str:
		""" 
		Request to bibleserver with the choosen Bibleversion.
		Returns the verse and improves self.chapter.
		"""
		r = requests.get("https://www.bibleserver.com/"+self.version+"/"+self.chapter)
		if r.status_code != 200:
			return False, "Fehler... Buch / Kapitel existiert nicht!"
		
		#Parse the html and find all spans
		soup = BeautifulSoup(r.text, 'html.parser')
		spans = soup.find_all("span", class_="verse-content--hover")
		
		#Build Verse
		verse = ""
		if len(self.versenumber) == 1:
			try:
				verse = spans[int(self.versenumber[0])-1].text
			except IndexError: return False, "Versnummer zu hoch"
			except: return False, "Fehler... Versnummer ist keine Zahl"
		else:
			try:
				for n in range(int(self.versenumber[0]), int(self.versenumber[1])+1):
					verse = verse + " " + spans[int(n)-1].text
			except IndexError: return False, "Versnummer zu hoch"
			except: return False, "Fehler... Versnummer ist keine Zahl"
		
		#Improve chapter
		h1 = soup.find_all("h1")
		if len(h1) == 1:
			self.chapter = h1[0].text.strip()
			if "." in self.chapter: self.chapter = self.chapter.replace(".", ". ")

		return True, verse

	def __repr__(self) -> str:
		return f"{self.location}: {self.verse}"

def main():
	#Create Bibleverse Object
	bibleverse = BibleSearch()
	bibleverse.Set_Verse()
	print(bibleverse)

if __name__ == "__main__":
	main()