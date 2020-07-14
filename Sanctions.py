import requests
import csv
import numpy as np

class Sanctions:
    requestedData = []
    sanctionsData = []
    outputData = []
    #Calculates levenshtein distance https://en.wikipedia.org/wiki/Levenshtein_distance
    def levenshtein(self,seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros ((size_x, size_y))
        for x in range(size_x):
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:
                    matrix [x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + 1,
                        matrix[x-1,y-1] + 1,
                        matrix[x,y-1] + 1
                    )
        return (matrix[size_x - 1, size_y - 1])

    #Grab input from server
    def getInput(self,url):
        resp = requests.get(url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /cloud/ {}'.format(resp.status_code))
        for todo_item in resp.json():
            self.requestedData.append(todo_item)

    #Read CSV for anything sanctioned
    def getSanctions(self):
        with open('sanctions.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        data = data[0]
        self.sanctionsData = data

    #Check For any similarities
    def checkSanctions(self):
        for req in self.requestedData:
            #Keep Track of the highest hit rate
            max_match = 0.0
            max_element1 = ""
            max_element2 = ""
            #Find Highest match rate
            for sanc in self.sanctionsData:
                distance = self.levenshtein(req,sanc)
                larger = max(len(req),len(sanc))
                if((larger - distance)/larger > max_match):
                    max_match = (larger - distance)/larger
                    max_element1 = req
                    max_element2 = sanc
            #Determine if that percent is high enough to be a hit
            if(max_match >= 0.75):
                print("Hit", max_element1, max_element2, round(max_match,3))
                self.outputData.append(str(max_element1 + " "+ max_element2))
            else:
                print("No Hit", max_element1, max_element2, round(max_match,3))


    def __init__(self,url):
        self.getInput(url)
        self.getSanctions()
        self.checkSanctions()

new_RTA = Sanctions("https://my-json-server.typicode.com/sohiladwani/insideSherpaModule2/input")
assert new_RTA.outputData[0] == "Iraan Iran"
assert new_RTA.outputData[1] == "Rusia Russia"
assert new_RTA.outputData[2] == "Adam Le Adam Lee"
assert new_RTA.outputData[3] == "akistan Pakistan"
assert new_RTA.outputData[4] == "Prance France"
assert new_RTA.outputData[5] == "North Koree North Korea"
assert new_RTA.outputData[6] == "Iraq Iran"
