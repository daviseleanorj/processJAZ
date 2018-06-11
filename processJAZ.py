import os,glob,sys,pandas,csv
from astropy.table import Table
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



###Read the data###
def readData(filename):
	return(ascii.read(filename))

###Change from .jaz to .txt###
def changeJAZ(folder):
	files=glob.glob(os.path.join(folder,'*.jaz'))
	for f in files:
		os.rename(f,f[:-3]+'txt')


###Change from .txt to .csv###
def changeCSV(filename):
	cfile= (filename[:-4]+".csv")
	txt_file= (r"C:\\Users\\Documents\\Folder\\"+filename)
	csv_file= (r"C:\\Users\\Documents\\Documents\\Folder\\"+cfile)
	in_txt = csv.reader(open(txt_file, "r"), delimiter = ' ')
	out_csv = csv.writer(open(csv_file, 'w'))
	out_csv.writerows(in_txt)


###Remove last line that is not data###
def removeLastLine(filename):
	cfile=(filename[:-4]+".csv")
	cnlfile=(filename[:-4]+"NL"+".csv")
	inCSV = open(cfile,'r')
	outCSV = open(cnlfile,'w')
	all_lines = inCSV.readlines()
	all_lines.pop(len(all_lines)-2)
	inCSV.close()

	with outCSV as out:
		for line in all_lines:
			out.write(line.strip()+ "\n")


###Remove beginning lines that are not data###
def removeLine(filename):
	cnlfile=(filename[:-4]+"NL"+".csv")
	cnflfile=(filename[17:-4]+"NFL"+".csv")
	inCSV = open(cnlfile,'r')
	outCSV = open(cnflfile,'w')
	all_lines = inCSV.readlines()

	# with outCSV as out:
	# 	out.writelines(np.append(all_lines[34],all_lines[585:1179]))
	# sys.exit()
	with outCSV as out:
		out.writelines(all_lines[33:1179])

###Insert header with filename/date###
def insertHeader(filename):
	cnflfile=(filename[:-4]+"NFL"+".csv")
	cihfile=(filename[:-4]+"IH"+".csv")
	inCSV=open(cnflfile,'r+')
	outCSV=open(cihfile, 'w')
	lines = inCSV.readlines()
	with outCSV as out:
		inCSV.seek(0)
		out.write('#'+filename[23:-4])
		for line in lines:
			out.write(line)

####Remove spaces between lines####
def removeSpace(filename):
	cihfile=(filename[:-4]+"IH"+".csv")
	# cns2file= (r"C:\\Users\\eleanord\\Documents\\JAZ spectrum\\"+"test"+filename[24:-4]+".csv")
	# cns2file= (r"C:\\Users\\eleanord\\Documents\\JAZ spectrum\\09162017\\finalSpec\\"+loc+"0916"+filename[17:-4]+".csv")
	# cns2file= (r"C:\\Users\\eleanord\\Documents\\JAZ spectrum\\12052017\\finalSpec\\"+loc+"1205"+filename[17:-4]+".csv")
	cns2file= (r"C:\\Users\\eleanord\\Documents\\JAZ spectrum\\FieldTestAlt\\finalSpec\\DarkAltTooley11205Spec0074.csv")
	inCSV = open(cihfile,'r')
	outCSV = open(cns2file,'w')
	writer = csv.writer(outCSV)
	for row in csv.reader(inCSV):
		if any(row):
			writer.writerow(row)


###Calculate reflectance####	
def calcReflectance(table,filename):
	#Calculate dark
	# table ['reflectance']=table['P']

	#Calculate reference
	# table ['reflectance']=table['R']

	# Calculate reflectance
	table ['reflectance']=table['R']-table['D']
	table=table[table['reflectance']!=0]
	table['reflectance']=(((table['S']-table['D'])/(table['R']-table['D']))*100)
	# specFilt=np.array(table['reflectance'])
	# print(specFilt)
	# specFilt=signal.medfilt(specFilt,kernel_size=11)
	return(table)

####Plot reflectance or reference or dark spectra###
def plotReflectance(tables,loc,filename,xmin=None,xmax=None):
	fig=plt.figure()
	ax=fig.gca()
	if not isinstance(tables,list):
		tables=[tables]
	for table in tables:
		if not xmin:
			xmin=0
		if not xmax:
			xmax=np.inf
		tempTable=table[table['W']<=xmax]
		tempTable=tempTable[tempTable['W']>=xmin]
		ax.plot(tempTable['W'],tempTable['reflectance'])
		ax.set_xlabel('Wavelength (nm)')
	# For Dark
	# ax.set_ylabel('Intensity (Units)')
	# ax.set_title('Dark Spectrum '+filename)

	# For Reference
	# ax.set_ylabel('Intensity (Units)')
	# ax.set_title('Reference for Spectrum '+filename)

	# For Reflectance
	ax.set_ylabel('Total Reflectance (%)')
	ax.set_title('Layered Reflectance')
	
	#plt.xticks(np.arange(np.round(table['W'][0]),np.round(table['W'][-1])+1,100))
	plt.locator_params(numticks=10)
	plt.savefig(os.path.join(loc,filename+'merged.png'),format='png',overwrite=True)


def main():
	locations=['folder1','folder2','folder3']

	for loc in locations:
		files=glob.glob(os.path.join('ALL',loc,'*.csv'))
		dataList=[]
		for f in files:
			changeJAZ(os.path.join('TestData',loc))
			changeCSV(f)
			removeLastLine(f)
			removeLine(f)
			insertHeader(f)
			removeSpace(f,loc)
			data=readData(f)
			table=calcReflectance(data,f)
			dataList.append(table)
		plotReflectance(dataList,os.path.join('ALL','outfolder'),os.path.basename(f)[:-4],xmin=400,xmax=750)



if __name__ == "__main__":

	main()
	sys.exit()