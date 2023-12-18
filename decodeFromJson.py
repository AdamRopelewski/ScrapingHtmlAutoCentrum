import jsonpickle



class CarModelGenerationLift:
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
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        

ListOfCarBrands=[]
print(ListOfCarBrands)



json_string = jsonpickle.encode(ListOfCarBrands)

try:
    f = open("ListOfCarBrands.json", "r")
    ListOfCarBrands = jsonpickle.decode(f.read())
finally:
    f.close()

print("")
