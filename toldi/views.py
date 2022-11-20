import json
import locale
import requests
import xml.etree.ElementTree as ET
from django.shortcuts import redirect, render
from django.utils.timezone import datetime
from django.views.generic import ListView
from requests.auth import HTTPBasicAuth
from django.views.decorators.csrf import csrf_exempt

from toldi.models import CNjoke, LogMessage  #, Country
from toldi.forms import CNjokeForm, LogMessageForm  #, CountryForm

"""from django. import requests

url = "https://google-translate1.p.rapidapi.com/language/translate/v2/detect"
xmlstring = "q=English%20is%20hard%2C%20but%20detectably%20so"
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"Accept-Encoding": "application/gzip",
	"X-RapidAPI-Key": "2043cfec63mshd0d2bef7c40fd92p1e88a5jsn8a7ceb4991ab",
	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
}
response = requests.request("POST", url, data=xmlstring, headers=headers)
print(response.text)"""


class HomeListView(ListView):
    """Renders the home page, with a list of all polls."""
    model = LogMessage
    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


def log_message(request):
    form = LogMessageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
        else:
            return render(request, "toldi/log_message.html", {"form": form})
    else:
        return render(request, "toldi/log_message.html", {"form": form})

    
class cnjokeListView(ListView):
    """Renders the ncjoke page, with a list of all jokes."""
    model = CNjoke
    def get_context_data(self, **kwargs):
        context = super(cnjokeListView, self).get_context_data(**kwargs)
        return context


@csrf_exempt
def cnjoke(request):
    """Renders the ncjoke page."""
    joke_list = CNjoke.objects.all()  #.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    #joke_list = ', '.join([q.theJoke for q in querySet_CNjoke])
    form = CNjokeForm(request.POST or None) 
    if request.method == "POST":
        #if form.is_valid():
            #joke = form.save(commit=False)
            #joke.theJoke = "json.loads(joke)"
            """url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
            xmlstring = "source=en&target=hu&q=English%20is%20hard%20for%20me"
            headers = {
            	"content-type": "application/x-www-form-urlencoded",
            	"Accept-Encoding": "application/gzip",
            	"X-RapidAPI-Key": "2043cfec63mshd0d2bef7c40fd92p1e88a5jsn8a7ceb4991ab",
            	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
            }           
            response = requests.request("POST", url, data=xmlstring, headers=headers) 
            joke = CNjoke(theJoke = response.json()["data"]["translations"][0]["translatedText"]) #{"data":{"translations":[{"translatedText":"Az angol nehéz"}]}}"""
            # webMetods / elsoProjekt
            #url = "https://env324825.int-aws-de.webmethods.io/integration/restv2/development/fl9f8b8f988366c117f46595/RestAPI/ChuckNorrisJoke"
            # webMetods / masodikProjekt
            url = "https://env324825.int-aws-de.webmethods.io/integration/restv2/development/flf22cc4a7bbd3b6320794d4/restAPIs/ChuckNorrisJoke"
            response = requests.request("GET", url, auth=HTTPBasicAuth('petrencerud@gmail.com', 'Petrence1234!'))
            if response.status_code == 200:
                joke = CNjoke(jokeEN = response.json()["joke_en"], jokeHU = response.json()["joke_hu"])
            else:
                joke = CNjoke(errorMsg = json.dumps( response.json() ) )
            joke.save()
            return render(request, "toldi/cnjoke.html", {"form": form, "joke_list":joke_list})  #redirect("home")
        #else:
        #    return render(request, "toldi/cnjoke.html", {"form": form, "joke_list":joke_list})  #, "joke_list": joke_list})
    else:
        return render(request, "toldi/cnjoke.html", {"form":form, "joke_list":joke_list})


def home(request):
    """Renders the about page."""
    return render(request, "toldi/home.html")


def about(request):
    """Renders the about page."""
    return render(request, "toldi/about.html")


def toldi_there(request, name):
    """Renders the toldi_there page.
    Args:
        name: Name to say toldi to
    """
    return render(
        request, "toldi/toldi_there.html", {"name": name, "date": datetime.now()}
    )


@csrf_exempt
def country(request):
    """Renders the country page.
    Args:
        name: country name to display details about
    """
    name = ''
    if request.method == 'POST':
        name = request.POST.get('name')
    #print("Request for country page received with name=%s" % name)
    #wsdl = 'https://env324825.int-aws-de.webmethods.io/integration/ws/development/flf22cc4a7bbd3b6320794d4/soapAPIs?wsdl'
    #client = SoapClient(wsdl=wsdl, username='petrencerud@gmail.com', password='Petrence1234!')
    # structured XML
    xmlstring = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:gs="http://toldi/soapws/gs_toldi_soap_ws">
                <soapenv:Header/>
                <soapenv:Body>
                    <gs:getCountryRequest>
                        <gs:name>"""+name+"""</gs:name>
                    </gs:getCountryRequest>
                </soapenv:Body>
            </soapenv:Envelope>""" #).strip() #.translate({ord(c):None for c in ' \n\t\r'})
    xmlstring = '<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:gs="http://toldi/soapws/gs_toldi_soap_ws"><soapenv:Header/><soapenv:Body><gs:getCountryRequest><gs:name>'
    xmlstring += name+'</gs:name></gs:getCountryRequest></soapenv:Body></soapenv:Envelope>'
    xmlstring = xmlstring.encode('utf-8')
    # headers
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    url = "https://env324825.int-aws-de.webmethods.io/integration/ws/development/flf22cc4a7bbd3b6320794d4/soapAPIs/CountriesPortSoap11"
    response = requests.request("POST", url, headers=headers, data=xmlstring, auth=HTTPBasicAuth('petrencerud@gmail.com', 'Petrence1234!'))
    if response.status_code == 200 :
        #tree = ET.ElementTree(ET.fromstring(response.text))
        root = ET.fromstring(response.text)
        countryName = root.find('.//{http://toldi/soapws/gs_toldi_soap_ws}name').text
        countryPopulation = root.find('.//{http://toldi/soapws/gs_toldi_soap_ws}population').text
        countryCapital = root.find('.//{http://toldi/soapws/gs_toldi_soap_ws}capital').text
        countryCurrency = root.find('.//{http://toldi/soapws/gs_toldi_soap_ws}currency').text
        if countryPopulation :
            locale.setlocale(locale.LC_ALL, '')
            countryPopulation = "{0:n}".format( int( countryPopulation ) )
        context = {"countryName":countryName, "countryPopulation":countryPopulation, "countryCapital":countryCapital, "countryCurrency":countryCurrency}
        return render( request, "toldi/country.html", context )
    else:
        return render( request, "toldi/country.html", {"error":response.text} )


""" if request.method == 'POST':
        name = request.POST.get('name')
        if name is None or name == '':
            print("Request for country page received with no name or blank name -- redirecting")
            #return redirect('...')
        else:
            print("Request for country page received with name=%s" % name)
            context = {'name': name }
            return render(request, 'toldi/country.html', context)
    else:
        return redirect('...')
"""    

