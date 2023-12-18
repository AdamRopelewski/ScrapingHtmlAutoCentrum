import jsonpickle



class CarModelGenerationVersion:
    def __init__(self, name, url) -> None:
        self.name= self.deleteWhiteSpace(name)
        self.url = url
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name
    def deleteWhiteSpace(self, name:str):
        outputList =[]
        for chr in name:
            if ord(chr)!= 32 and ord(chr)!=10:
                outputList.append(chr)
        return ''.join(outputList)


class CarModelGeneration:
    def __init__(self, name, url) -> None:
        self.name= self.deleteWhiteSpace(name)
        self.listOfVersions=[]
        self.url = url
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name
    def addVersion(self, CarModelGenerationVersion: CarModelGenerationVersion):
        self.listOfVersions.append(CarModelGenerationVersion)
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
        return self.name 
    def __repr__(self) -> str:
        return self.name +", "+ str(self.listOfGenerations)

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
        return self.name +", " + str(self.listOfModels)



def openAndDecodeJson(path:str)->list:
    try:
        f = open(path, "r")
        ListOfCarBrands = jsonpickle.decode(f.read())
    finally:
        f.close()
    return ListOfCarBrands

def convertListOfCarBrandsToCSV(ListOfCarBrands:list, path:str)->None:
    output=[]
    for brand in ListOfCarBrands:
        for model in brand.listOfModels:
            for generation in model.listOfGenerations:
                for version in generation.listOfVersions:
                    output.append(f"{brand.name}; {model.name}; {generation.name}; {version.name}\n")

    try:
        f = open(path, "w")
        f.write(''.join(output))
    finally:
        f.close()
