import requests
from bs4 import BeautifulSoup

class CarModelGeneration:
    def __init__(self, name, url) -> None:
        self.name= self.deleteWhiteSpace(name)
        self.url = url
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return "\n" + self.name
    def deleteWhiteSpace(self, name:str):
        outputList =[]
        for chr in name:
            if ord(chr)!= 32 and ord(chr)!=10:
                outputList.append(chr)
        return ''.join(outputList)

class CarModel:
    def __init__(self, name, url) -> None:
        self.name= name
        self.listOfGenerations=[]
        self.url = url
    def addGeneration(self, CarModelGeneration: CarModelGeneration):
        self.listOfGenerations.append(CarModelGeneration)
    def __str__(self) -> str:
        # return self.name +": \n"+ str(self.listOfGenerations)
        return self.name 
    def __repr__(self) -> str:
        return self.name +":"+ str(self.listOfGenerations)

class CarBrand:
    def __init__(self, name, url) -> None:
        self.name = name
        self.listOfModels= []
        self.url = url
    def addCarModel(self, CarModel: CarModel):
        self.listOfModels.append(CarModel)
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name +": " + str(self.listOfModels)
        

page_url="https://www.autocentrum.pl/dane-techniczne"
main_page_url = "https://www.autocentrum.pl"

ListOfCarBrands=[]


page = requests.get(page_url)
soup = BeautifulSoup(page.content, 'html.parser')


output = soup.find_all("div", {"class": 'make-wrapper popular-make'})
output += soup.find_all("div", {"class": 'make-wrapper not-popular-make'})

for i in range(len(output)):
    name = str(output[i].contents[1].contents[3])
    name = name[19:]
    name = name[:-7]
    url = main_page_url + output[i].contents[1].attrs['href']

    ListOfCarBrands.append(CarBrand(name, url))

for car in ListOfCarBrands[0:1]:
    page = requests.get(car.url)
    soup = BeautifulSoup(page.content, 'html.parser')
    output = soup.find("div", {"class": 'car-selector-box-row'})
    outputUrls = output.find_all("a", href=True)
    outputNames = output.find_all("h2", {"class": 'name-of-the-car'})

    for i in range(len(outputNames)):
        url = main_page_url + outputUrls[i].attrs['href']
        car.addCarModel(CarModel(outputNames[i].contents[0].strip(), url))

for car in ListOfCarBrands[0:1]:
    for model in car.listOfModels:
        page = requests.get(model.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            output = soup.find("div", {"class": 'car-selector-box-row active'})
            outputUrls = output.find_all("a", href=True)
            outputNames = output.find_all("h2", {"class": 'name-of-the-car'})
        except AttributeError:
            continue


        for i in range(len(outputNames)):
            url = main_page_url + outputUrls[i].attrs['href']
            model.addGeneration(CarModelGeneration(outputNames[i].contents[0].strip(), url))


print(ListOfCarBrands[0:1])
print("")