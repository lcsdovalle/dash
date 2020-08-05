import requests



class PyWebService():
    def __init__(self,link,params):
        self.webservice = link
        self.params = params
    def run(self):
        params = "?"
        for p in self.params:
            params += "&"+str(p)
        params = params.replace("?&","?")
        # result = requests.get(webservice+"classid="+classid+"&subject="+subject+"&token="+token+"&takeout="+takeout).json()
        # params = params.replace('*')
        request = self.webservice+params
        print(request)
        return requests.get(self.webservice+params).json()
# params = []

# params.append("type=totalClass")
# params.append("client=Camaçari")
# params.append("100=Camaçari")
# web = PyWebService('http',params)
# print(web.run())