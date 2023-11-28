import xml.etree.ElementTree as ET
import xml.dom.minidom 

def readInput(hamNotation, dictGloss, compound):
	global data, glosses_sigml, hasGlosses

	data = ET.Element('sigml')
	glosses_sigml = []
	inputContent = hamNotation

	if len(inputContent) > 1:					
		hasGlosses = True	
		hamnosysContent = inputContent[0].split(" ")
		glossesList = inputContent[1].split(" ")
	else:										
		hasGlosses = False				
		hamnosysContent = inputContent[0].split(" ")
	
	codesList = []
	for char in hamnosysContent:
		hamnosysCode = char.encode('unicode_escape').decode()	
		hamnosysCode = hamnosysCode.replace("\\u", "")
		hamnosysCode = hamnosysCode.upper()
		codesList.append(hamnosysCode)


	if hasGlosses:
		codesList = readLists(glossesList, codesList, dictGloss, compound)	
	else:
		codesList = readLists(None, codesList, dictGloss, compound)


def readLists(glosses, codes, dictGloss, compound):	
	if hasGlosses:
		glosses_hamnosys = [(glosses[i], codes[i]) for i in range(0, len(codes))]

		for i in range(0, len(glosses_hamnosys)):
			aux = hamnosysList(glosses_hamnosys[i][1])
			readCode(glosses_hamnosys[i][0], aux)
	else:
		glosses_hamnosys = [(None, codes[i]) for i in range(0, len(codes))]		
		count = 1
		for i in range(0, len(glosses_hamnosys)):
			aux = hamnosysList(glosses_hamnosys[i][1])

			readCode(count, aux)	
			count += 1

	writeSiGML(glosses_sigml, dictGloss, compound)


def hamnosysList(codes):
	hamnosys_list = []
	n = 4 

	for j in range(0, len(codes), n):
		singleCode = codes[j:j+n]
		hamnosys_list.append(singleCode)

	return hamnosys_list

def readCode(gloss, hamnosys):
	conversionTXT = "conversionSpreadSheet.txt"
	sigmlList = []

	with open(conversionTXT, 'r') as f:
		for code in hamnosys:
			f.seek(0)
			for line in f:
				if code in line:
					fields = line.split(",")
					sigmlList.append(fields[0])
					break


	for i in range(0, len(sigmlList)):
		glosses_sigml.append((gloss, sigmlList[i]))


def writeSiGML(thisdict, dictGloss, compound):
	previousGloss = "null"

	for i in range(0, len(thisdict)):
		if(previousGloss == thisdict[i][0]):
			ET.SubElement(itemManual, thisdict[i][1])
		else:
			itemGloss = ET.SubElement(data, 'hns_sign')
			itemGloss.set('gloss', dictGloss)			
			if(hasGlosses):
				itemGloss.set('gloss', thisdict[i][0])			
			
			itemNonManual = ET.SubElement(itemGloss, 'hamnosys_nonmanual')
			itemManual = ET.SubElement(itemGloss, 'hamnosys_manual')

			mouth = ET.SubElement(itemNonManual, "hnm_mouthpicture")
			brows = ET.SubElement(itemNonManual, "hnm_eyebrows")
			nose = ET.SubElement(itemNonManual, "hnm_nose")
			eyes = ET.SubElement(itemNonManual, "hnm_eyelids")
			mouth.set('picture', dictGloss[:5])
   
			if(compound > 0.05):
				brows.set('tag', "RB")
				eyes.set('tag', "WB")
			elif(compound < -0.05):
				brows.set('tag', 'FU')
				nose.set('tag', 'WR')
				eyes.set('tag', 'SB')
			else:
				eyes.set('tag', 'BB')
				
			ET.SubElement(itemManual, thisdict[i][1])

		previousGloss = thisdict[i][0]

	dataStr = ET.tostring(data, encoding='unicode')
	dom = xml.dom.minidom.parseString(dataStr)
	aux = dom.toprettyxml(encoding='UTF-8').decode("utf-8")
	
	splitAux = aux.split('\n')

	with open("static/sigml/SiGML-output.sigml", "a") as f:
		f.write('\n')
		f.write('\n'.join(splitAux[2:-2]))


