def word_tokenizer(sentence):
	tokens = []
	for word in sentence.split():
		found_mutliple_token = False
		word = word.replace('–', '-')
		for i in range(0, len(word)):

			# for words that contain multiple cities, organisations, etc
			# e.g. Avstriya-Macarıstan | Molotov-Ribbentrop | Berlin-Bonn
			# ignored words | e.g. emin-amanliq | bir-birilərinə | əks-hücum
			if word[i] == "-" and word[i+1].isalpha() and word[i-1].isalpha() and word[i+1].isupper() and word[0].isupper() and word.count('-') == 1:
				if word.count("Nyu-York") != 0:
					tokens.append(word)
					found_mutliple_token = True
					break
				tokens.append(word[:i])
				tokens.append("-")
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for words that contain 3 cities, organisations, etc
			# e.g. Bakı-Tbilisi-Qars
			# ignored words | e.g. emin-amanliq | bir-birilərinə | əks-hücum
			if word[i] == "-" and word[i+1].isalpha() and word[i-1].isalpha() and word[i+1].isupper() and word[0].isupper() and word.count('-') == 2:
				tokens.append(word[:i])
				tokens.append(word[i])
				for j in range(i+1, len(word)):
					if word[j] == "-" and word[j-1].isalpha() and word[j+1].isalpha():
						tokens.append(word[i+1:j])
						tokens.append(word[j])
						tokens.append(word[j+1:])
				found_mutliple_token = True
				break


			# for multiple years/numbers
			# e.g. 25–27 | 1925-1927
			elif word[i] == "-" and word[i+1].isnumeric() and word[i-1].isnumeric() and word.count("-") == 1:
				tokens.append(word[:i])
				tokens.append(word[i])
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for words that contain organisations
			# e.g. NATO-ya | SSRİ-nin
			# ignored words | e.g. emin-amanliq | bir-birilərinə | əks-hücum | Avstriya-Macarıstan (since checked previously)
			elif word[i] == "-" and word[i+1].isalpha() and word[i-1].isalpha() and word[0].isupper() and word[i+1].islower() and word.count('-') == 1:
				tokens.append(word[:i])
				tokens.append("-")
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for words that contain date starting after the actual word
			# e.g. sonra-10
			elif word[i] == "-" and word[i+1].isnumeric() and word[i-1].isalpha() and word.count("-") == 1:
				tokens.append(word[:i])
				tokens.append(word[i])
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for words that contain -
			# e.g. km²-i |
			# ignored words | e.g. anything that ends with -some letters start with lowercase letter
			elif word[i] == "-" and word[i+1].isalpha() and word[i+1].islower() and word[0].isalpha() and word.count('-') == 1 and len(word[i+1:])<=3:
				tokens.append(word[:i])
				tokens.append("-")
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for dates
			# e.g. 1914-cü | 
			# ignored words | e.g. bir-birilərinə | əks-hücum
			elif word[i] == "-"  and word[i+1].isalpha() and word.count('-') == 1 and word[0].isnumeric():
				tokens.append(word[:i])
				tokens.append("-")
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for dates, part 2
			# e.g. 1922–1923-cü |
			# ignored words | e.g. bir-birilərinə | əks-hücum
			elif word[i] == "-" and word[i-1].isnumeric() and word[i+1].isnumeric() and word.count('-') == 2:
				tokens.append(word[:i])
				tokens.append("-")
				for j in range(i+1, len(word)):
					if word[j] == "-" and word[j-1].isnumeric() and word[j+1].isalpha():
						tokens.append(word[i+1:j])
						tokens.append("-")
						tokens.append(word[j+1:])

				found_mutliple_token = True
				break
			# for dates that include sonra and year
			# e.g. sonra-2004-cü | 

			elif word[i] == "-" and word[i-1].isalpha() and word[i+1].isnumeric() and word.count('-') == 2:
				tokens.append(word[:i])
				tokens.append(word[i])
				for j in range(i+1, len(word)):
					if word[j] == "-" and word[j-1].isnumeric() and word[j+1].isalpha():
						tokens.append(word[i+1:j])
						tokens.append("-")
						tokens.append(word[j+1:])
				found_mutliple_token = True
				break

			# for words that contain - and ends with some letters like i | ni
			# it is not necessary that word starts with a letter or a number for this conditional statement
			# e.g. °C-dək |
			# ignored words | 
			elif word[i] == "-" and word[i+1].isalpha() and word[i+1].islower() and word.count('-') == 1 and len(word[i+1:]) <= 3:
				print("hello")
				tokens.append(word[:i])
				tokens.append("-")
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for sentence endings with .
			# e.g. başladı. | 
			# ignored words | e.g. 1.7 | 2.7
			elif word[i] == "." and word[i-1].isalpha() and word.count(".") == 1 and i + 1 == len(word) and word != "St.":
				tokens.append(word[:i])
				tokens.append(word[i])
				found_mutliple_token = True
				break

			# for sentence endings with !
			# e.g. sökün! | 
			# ignored words 
			elif word[i] == "!" and word[i-1].isalpha() and word.count("!") == 1 and i + 1 == len(word):
				tokens.append(word[:i])
				tokens.append(word[i])
				found_mutliple_token = True
				break

			# for comma separation
			# e.g. olaraq, | 
			# ignored words | e.g. 30,000 | 220,000 | 1,500,000
			elif word[i] == "," and word[i-1].isalpha() and word.count(",") == 1:
				tokens.append(word[:i])
				tokens.append(word[i])
				found_mutliple_token = True
				break

			# for years that end with comma
			# e.g. 2015, | 
			elif word[i] == "," and word[i-1].isnumeric() and word.count(",") == 1 and len(word) == 5 and i == len(word) - 1:
				tokens.append(word[:i])
				tokens.append(word[i])
				found_mutliple_token = True
				break

			# for quoted word combinations (starting quotes)
			# e.g. "qismən
			elif word[i] == '"' and i == 0 and len(word) >=2 and word[i+1].isalpha() and word.count('"') == 1:
				tokens.append(word[i])
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for quoted word combinations (ending quotes)
			# e.g. stabilləşmə" |
			elif word[i] == '"' and i != 0 and word[i-1].isalpha() and word.count('"') == 1 and i == len(word) - 1:
				tokens.append(word[:i])
				tokens.append(word[i])
				found_mutliple_token = True
				break

			# for quoted word combinations (ending quotes) that does not end with the quote
			# e.g.  pərdə"ni  |
			elif word[i] == '"' and i != 0 and word[i-1].isalpha() and word.count('"') == 1 and i != len(word) - 1 and word[i+1:].isalpha():
				tokens.append(word[:i])
				tokens.append(word[i])
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for quoted word combinations (quotes that contain one word)
			# e.g. "Ostpolitik" |	
			elif word[i] == '"' and word.count('"') == 2:
				tokens.append(word[i]) # first "
				tokens.append(word[i+1:-1]) # the word until ending "
				tokens.append(word[-1]) # last "
				found_mutliple_token = True
				break

			# for quoted word combinations (ending quotes) that has sentence endings such as . or !
			# e.g. sökün!" | 
			elif word[i] == '"' and i != 0 and i != len(word) - 1 and word[i-1] in ("!" or ".") and word.count('"') == 1:
				tokens.append(word[:i-1]) # until the sentence ending ! or .
				tokens.append(word[i-1]) # sentence ending ! or .
				tokens.append(word[-1]) # quote
				found_mutliple_token = True
				break

			# for quoted word combinations (ending quotes) that has sentence ending after the quote
			# e.g. bilər". |
			elif word[i] == '"' and i != 0 and (word[i+1] == "." or word[i+1] == "!" or word[i+1] == ",") and word.count('"') == 1:
				tokens.append(word[:i]) # until the sentence ending ! or .
				tokens.append(word[i]) # "
				tokens.append(word[i+1]) # . or !
				found_mutliple_token = True
				break

			# for paranthesis (starting parenthesis)
			# e.g. (əhalinin | 
			elif word[i] == "(" and i == 0 and len(word) >=2 and word[i+1].isalpha() and word.count("(") == 1 and word.count(")") == 0:
				tokens.append(word[i])
				tokens.append(word[i+1:])
				found_mutliple_token = True
				break

			# for paranthesis (ending parenthesis)
			# e.g. faizi) | 
			elif word[i] == ")" and i != 0 and word[i-1].isalpha() and word.count(")") == 1 and word.count("(") == 0:
				tokens.append(word[:i])
				tokens.append(word[i])
				found_mutliple_token = True
				break

			# for paranthesis (paranthesis that contain one word)
			# e.g. (NATO) |	(YAP) | 
			elif word[i] == '(' and word.count('(') == 1 and word.count(')') == 1 and word[-1] == ')' and word.count("-") == 0:
				tokens.append(word[i]) # first (
				tokens.append(word[i+1:-1]) # the word until ending )
				tokens.append(word[-1]) # last "
				found_mutliple_token = True
				break

			# for paranthesis (paranthesis that contain years)
			# e.g. (2005–2007)
			elif word[i] == '(' and word.count('(') == 1 and word.count(')') == 1 and word[-1] == ')' and word.count("-") == 1 and word.count(",") == 0:
				tokens.append(word[i]) # first (
				for j in range(i+1, len(word)):
					if word[j] == "-":
						tokens.append(word[i+1:j])
						tokens.append(word[j])
						tokens.append(word[j+1:-1])
						tokens.append(word[-1])
						break
				found_mutliple_token = True
				break

			# for paranthesis (paranthesis that contain years)
			# e.g. (2005–2007),
			elif word[i] == '(' and word.count('(') == 1 and word.count(')') == 1 and word[-2] == ')' and word.count("-") == 1 and word.count(",") == 1:
				tokens.append(word[i]) # first (
				for j in range(i+1, len(word)):
					if word[j] == "-":
						tokens.append(word[i+1:j])
						tokens.append(word[j])
						tokens.append(word[j+1:-2])
						tokens.append(word[-2])
						tokens.append(word[-1])
						break
				found_mutliple_token = True
				break

			# for paranthesis (starting parenthesis) that contains year
			# e.g. (2019-cu | 
			elif word[i] == "(" and i == 0 and len(word) >=2 and word[i+1].isnumeric() and word.count("(") == 1 and word.count('-') == 1:
				tokens.append(word[i])
				tokens.append(word[i+1:word.index('-')])
				tokens.append('-')
				tokens.append(word[word.index('-') + 1:])
				found_mutliple_token = True
				break

			# for colon endings
			# e.g. yaşama:
			elif word[i] == ":" and i == len(word) - 1:
				tokens.append(word[:i])
				tokens.append(word[i])
				found_mutliple_token = True
				break

		# if we did not find a word that contains multiple tokens
		# meaning that word itself is a token
		# e.g. nəticəsində | müharibəsi
		if not found_mutliple_token:
			tokens.append(word)
	return tokens

# IGNORED: "Bakı-İslam