# -*- coding: utf-8 -*-
import os, requests, uuid, json, sys

""" Imports environment variables from operating system with specified names 
    (Further explained if you go through tutorials on Bing API) """

key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

translateAll = input("Translate all text in file to language of choice? (y/n): ")
if translateAll not in ['y', 'n']:
	raise Exception("y or n wasn't inserted. Please insert either of these two choices.")

# Request below scrapes all languages Bing translator can perform on
languageURL = "https://api.cognitive.microsofttranslator.com/languages?api-version=3.0"
param = {'api-version': '3.0', 'scope': 'translation'}
getRequest = requests.get(languageURL, param)
langAbr = getRequest.json()['translation'].keys()

if "n" in translateAll:
	langOfFile = input("Which language in the text do you want to translate? (in Abbreviation): ")
	if langOfFile not in langAbr:
		raise Exception("Incorrect abbreviation was provided, please provide right one.")

langOfTs = input("Which language do you wish to translate the text into? (in Abbreviation): ")
if langOfFile not in langAbr:
	raise Exception("Incorrect abbreviation was provided, please provide right one.")

# Constructs URL neccesary for Bing translation to undergo
path = '/translate?api-version=3.0'
translateto = '&to=' + langOfTs
constructed_url = endpoint + path + translateto

destPath = input("Enter path of directory where file is present: ")

files = [f for f in os.listdir(destPath) if os.path.isfile(os.path.join(destPath, f))]

ALLOWEDEXTENSIONS = ['.txt', '.ks']
DIRECTORYNAME = 0
filesTranslated = 1
varname = "file"

# Translates all files in given directory iff file is of appropriate extension
for file in files:
	foundextension = None
	for extension in ALLOWEDEXTENSIONS:
		if extension in file:
			foundextension = extension
			break
	if foundextension == None:
		continue

	# For purposes of opening and creating translated file
	splitfile = file.split(extension)
	revamp = destPath + '/' + splitfile[DIRECTORYNAME] + "trans" + foundextension
	originfile = open(destPath + '/'+ file, "r", encoding = 'utf-8')
	revampfile = open(revamp, "w", encoding = 'utf-8')

	for line in originfile.readlines():
		body1 = [{'text': line}]
		request = requests.post(constructed_url, headers = headers, json = body1)
		response = request.json()

		# Tries to retrieve translation of current line in file using Bing translater
		try:
			languageInText = response[0]["detectedLanguage"]["language"]

		# Error occurs when indexing can't be accessed 
		except KeyError:
			print("The Bing Translator can't be accessed (Either you ran out of credits (to translate) or something went wrong in Bing's server")
		else:
			if langOfFile in languageInText or translateAll == "y":
				revampfile.write(response[0]["translations"][0]["text"])
			else:
				revampfile.write(line) 

	print("{} {} has been translated".format(filesTranslated, varname))

	if filesTranslated == 1:
		varname = varname + "s"

	revampfile.close()
	originfile.close()

print("Everything Translated!")

 
