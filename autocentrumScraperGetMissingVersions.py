import requests
from bs4 import BeautifulSoup
import time
import jsonpickle
from decodeFromJsonIntoCsv import openAndDecodeJson, convertListOfCarBrandsToCSV


class CarModelGenerationVersion:
    def __init__(self, name, url) -> None:
        self.name = self.deleteWhiteSpace(name)
        self.url = url

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def deleteWhiteSpace(self, name: str):
        outputList = []
        for chr in name:
            if ord(chr) != 32 and ord(chr) != 10:
                outputList.append(chr)
        return "".join(outputList)


class CarModelGeneration:
    def __init__(self, name, url) -> None:
        self.name = self.deleteWhiteSpace(name)
        self.listOfVersions = []
        self.url = url

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def addVersion(self, CarModelGenerationVersion: CarModelGenerationVersion):
        self.listOfVersions.append(CarModelGenerationVersion)

    def deleteWhiteSpace(self, name: str):
        outputList = []
        for chr in name:
            if ord(chr) != 32 and ord(chr) != 10:
                outputList.append(chr)
        return "".join(outputList)


class CarModel:
    def __init__(self, name, url) -> None:
        self.name = name
        self.listOfGenerations = []
        self.url = url

    def addGeneration(self, CarModelGeneration: CarModelGeneration):
        self.listOfGenerations.append(CarModelGeneration)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name + ", " + str(self.listOfGenerations)


class CarBrand:
    def __init__(self, name, url) -> None:
        self.name = name
        self.listOfModels = []
        self.url = url

    def addCarModel(self, CarModel: CarModel):
        self.listOfModels.append(CarModel)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name + ", " + str(self.listOfModels)


startTime = time.time()
page_url = "https://www.autocentrum.pl/dane-techniczne"
main_page_url = "https://www.autocentrum.pl"


# def reWriteTheObjectFromJson(ListOfCarBrands):
#     newListOfCarBrands=[]

#     for i in range(len(ListOfCarBrands)):
#         newListOfCarBrands.append(CarBrand(ListOfCarBrands[i].name, ListOfCarBrands[i].url))

#         for j in range(len(ListOfCarBrands[i].listOfModels)):
#             newListOfCarBrands[i].addCarModel(CarModel(ListOfCarBrands[i].listOfModels[j].name,
#                                                        ListOfCarBrands[i].listOfModels[j].url))

#             for k in range(len(ListOfCarBrands[i].listOfModels[j].listOfGenerations)):
#                 newListOfCarBrands[i].listOfModels[j].addGeneration(CarModelGeneration(
#                     ListOfCarBrands[i].listOfModels[j].listOfGenerations[k].name,
#                     ListOfCarBrands[i].listOfModels[j].listOfGenerations[k].url))


#     return newListOfCarBrands

# ListOfCarBrands = reWriteTheObjectFromJson(ListOfCarBrands)
ListOfCarBrands = []
# shouldLoad = ""
# shouldLoad = input("Czy ładować dane z pliku ListOfCarBrands.json? [Y/N]")
# if shouldLoad.lower() == "y" or shouldLoad.lower() == "t":
#     ListOfCarBrands = openAndDecodeJson("ListOfCarBrandsNEW.json")
ListOfCarBrands = openAndDecodeJson("ListOfCarBrandsNEW.json")


page = requests.get(page_url)
soup = BeautifulSoup(page.content, "html.parser")


output = soup.find_all("div", {"class": "make-wrapper popular-make"})
output += soup.find_all("div", {"class": "make-wrapper not-popular-make"})

# Loading CarBrands into the list
# for i in range(len(output)):
#     name = str(output[i].contents[1].contents[3])
#     name = name[19:]
#     name = name[:-7]
#     url = main_page_url + output[i].contents[1].attrs["href"]
#     newCarBrand = CarBrand(name, url)
#     ListOfCarBrands.append(newCarBrand)

print("All of the Car Brands names have been loaded.\n")

# Loading Models of the Brands into the list
# for brand in ListOfCarBrands[2:3]:
#     page = requests.get(brand.url)
#     soup = BeautifulSoup(page.content, "html.parser")
#     try:
#         output = soup.find("div", {"class": "car-selector-box-row"})
#         outputUrls = output.find_all("a", href=True)
#         outputNames = output.find_all("h2", {"class": "name-of-the-car"})
#     except AttributeError:
#         # If the page doesnt load - skip it
#         continue

#     for i in range(len(outputNames)):
#         url = main_page_url + outputUrls[i].attrs["href"]
#         newCarModel = CarModel(outputNames[i].contents[0].strip(), url)
#         if newCarModel not in brand.listOfModels:
#             brand.addCarModel(CarModel(outputNames[i].contents[0].strip(), url))
#     print(f"Finished adding model for: {brand.name}\n")

# Loading Generaton of the Models into the list
for brand in ListOfCarBrands:
    for model in brand.listOfModels:
        if len(model.listOfGenerations) != 0:
            continue
        page = requests.get(model.url)
        soup = BeautifulSoup(page.content, "html.parser")
        # try:
        #     # If Model has no generation - skip looking for them
        #     output = soup.find("div", {"class": "car-selector-box-row active"})
        #     outputUrls = output.find_all("a", href=True)
        #     outputNames = output.find_all("h2", {"class": "name-of-the-car"})
        # except AttributeError:
        #     continue
        # for i in range(len(outputNames)):
        #     url = main_page_url + outputUrls[i].attrs["href"]
        #     newCarModelGeneration = CarModelGeneration(
        #         outputNames[i].contents[0].strip(), url
        #     )
        #     model.addGeneration(newCarModelGeneration)
        # add place holder generation for cars that dont have one
        try:
            output = soup.find("div", {"class": "ar-selector-box-row active"})
            outputUrls = output.find_all("a", href=True)
            outputNames = output.find_all("h2", {"class": "name-of-the-car"})
        except AttributeError:
            if len(model.listOfGenerations) == 0:
                url = model.url
                model.addGeneration(CarModelGeneration("PlaceholderGen", url))
                print(f"Finished adding generations for: {brand.name}: {model.name}\n")
            continue


# Loading Versions of the Generations into the list
for brand in ListOfCarBrands:
    for model in brand.listOfModels:
        for generation in model.listOfGenerations:
            if generation.name != "PlaceholderGen":
                continue
            page = requests.get(generation.url)
            soup = BeautifulSoup(page.content, "html.parser")
            try:
                # If Model has no generation - skip looking for them
                output = soup.find("div", {"class": "car-selector-box-row"})
                outputUrls = output.find_all("a", href=True)
                outputNames = output.find_all("h2", {"class": "name-of-the-car"})
            except AttributeError:
                continue

            for i in range(len(outputNames)):
                url = main_page_url + outputUrls[i].attrs["href"]
                generation.addVersion(
                    CarModelGenerationVersion(outputNames[i].contents[0].strip(), url)
                )
            print(
                f"Finished adding version for: {brand.name}: {model.name}: {generation.name}\n"
            )

elapsed = time.time() - startTime
print(ListOfCarBrands)


print(f"\nCzas trwania: {elapsed}")
json_string = jsonpickle.encode(ListOfCarBrands)

try:
    f = open("ListOfCarBrandsWithMissingOnes.json", "w")
    f.write(json_string)
finally:
    f.close()
print("")


convertListOfCarBrandsToCSV(ListOfCarBrands, "ListOfCarBrandsWithMissingOnes.csv")
