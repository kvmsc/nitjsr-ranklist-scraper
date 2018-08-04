from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
import csv

rolls = []
result =[]
finalranks = []
branches={"1":"EC","2":"CS","3":"EE","4":"CE","5":"ME","6":"PI","7":"MM"}

"""Generates all the rollnumbers in the required batch and branch"""
def rollgen():
	print("--Select Branch--\n1)ECE\n2)CSE\n3)EEE\n4)Civil\n5)Mech\n6)PIE\n7)Meta")
	try:
		branch = branches[str(input("Enter Your Choice:"))]
	except:
		print("Maybe You're an idiot or Your branch doesn't exist in NITJSR!")
		exit()
	batch = str(input("Enter Your Batch:"))
	head = batch+"UG"+branch
	for i in range(1,101):
		rolls.append(head+str(i//100) +(str(i//10)+str(i%10)))
	return branch

"""This Function opens the result website and scrapes the name and his/her cgpa and stores it into a list of dicts"""
def resultgen():
	semester = str(input("Enter Semester Number(1-8):"))
	"""Set the visibility to 1 if you want to watch the scraping process"""
	display = Display(visible=1, size=(800, 600))
	display.start()
	"""To check whether chromedriver exists in your system"""
	try:
		driver = webdriver.Chrome("/usr/bin/chromedriver")
	except:
		print("Webdriver path needs to be changed or needs to be installed")
		exit()
	for roll in rolls:
		"""Tries to open the website and exits when the site is down"""
		try:
			sleep(2)
			driver.get("http://14.139.205.172/web_new/Default.aspx")
		except:
			print(" The Result Site is Down")
			exit()
		else:	
			r_element = driver.find_element_by_id('txtRegno')
			#r_element.click()
			r_element.send_keys(roll)
			r_element.send_keys(Keys.ENTER)
			"""This statement throws an exception when the student's result is not published. So when it throws we catch. Ain't?"""
			try:
				s_element = Select(driver.find_element_by_id('ddlSemester'))
			except:
				print(roll," Result Not Available")
				driver.switch_to_alert().accept()
			else:
				"""Checks Whether the input semester result is available or not"""
				try:
					s_element.select_by_value(semester)
				except:
					print(roll + " Result Not Available")
					pass					
				else:
					driver.find_element_by_id('btnimgShowResult').click()
					name = driver.find_element_by_id('lblStudentName').text
					cgpa = driver.find_element_by_id('lblCPI').text
					result.append({"name":name,"cgpa":cgpa,"roll":roll})

"""This function Saves the scraped data to a csv file"""
def printresult(branch):
	"""Sorting the results scraped"""
	finalranks=sorted(result,key=lambda k:k['cgpa'],reverse=(True))
	print()
	i=1
	for i in range(len(finalranks)):
		finalranks[i]['Rank']=str(i+1)
	keys = finalranks[0].keys()
	"""Writing the data to a CSV"""
	filename = "result"+branch+".csv"
	with open(filename,"w") as writeFile:
		writer = csv.DictWriter(writeFile,keys)
		writer.writeheader()
		writer.writerows(finalranks)

def main():
	branch = rollgen()
	resultgen()
	printresult(branch)

if __name__ == '__main__':
	main()
