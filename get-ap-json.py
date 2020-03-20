#!/usr/bin/env python
"""
Codigo utilizado para obtener el estado de una interfaces de un CSRv y luego parse la respuesta 
que esta en formato json, convertir en Dic para luego imprimir. una vex en dic se puede modificar 
convertir en json de vuelta y modificar el valor 

"""
import requests
import json
import xmltodict

url = "https://10.97.4.222/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1"

payload = {}
headers = {
  'Accept': 'application/yang-data+json',
  'Authorization': 'Basic Y2lzY286QzFzY28xMjM0NQ=='
}

response = requests.request("GET", url, headers=headers, data = payload, verify=False)  # response type <class 'requests.models.Response'>
response_string = response.text.encode('utf8')  #convierte en str la respuesta 
#print(response.text.encode('utf8'))

json_object = json.loads(response_string) # Parsie response_string y lo convierte en un dic <class 'dict'>


print(json.dumps(json_object, indent=4, sort_keys=True)) #dumps convierte python (dic to json)

print(json_object['Cisco-IOS-XE-native:GigabitEthernet'])

interfaces = json_object.get('Cisco-IOS-XE-native:GigabitEthernet')

int_IP = json_object["Cisco-IOS-XE-native:GigabitEthernet"]["ip"]["address"]["primary"]["address"] # de esta manera puedo ir iterando el json hasta llegar al valor que deseo
int_Mask = json_object["Cisco-IOS-XE-native:GigabitEthernet"]["ip"]["address"]["primary"]["mask"]



print('   Interfaces GigabitEthernet ' + interfaces['name'] + '   IP: ' + int_IP + '   Mask: ' + int_Mask)

#to modify values in the dic we can use : json_object["GigabitEthernet"]["ip"]["address"]["primary"]["address"] = "192.168.0.2" but i need to convert it back json use dumps
#print(json.dumps(json_object)) 
#------------------------------------------------------------.-.-.-.--------------------------------------.-.-.-.-.------------------------------------------.-..-----------

# Este codigo se puede mejorar bastante, como por ejemplo
# tener un archivo de requerimientos antes de ejecutar, realizar uso de una funcion, variales para que 
# sea reusable. utilizar las best practice de PEP8 https://www.python.org/dev/peps/pep-0008/

# Realizar el mismo request pero en xml 


headers2 = {
  'Accept': 'application/yang-data+xml',
  'Authorization': 'Basic Y2lzY286QzFzY28xMjM0NQ=='
}

response_xml = requests.request("GET", url, headers=headers2, data = payload, verify=False)

response_string_xml = response_xml.text.encode('utf8')

xml_response = xmltodict.parse(response_string_xml) # crear a order dic 

xml_name = xml_response["GigabitEthernet"]["name"]

xml_IP = xml_response["GigabitEthernet"]["ip"]["address"]["primary"]["address"]

xml_Mask = xml_response["GigabitEthernet"]["ip"]["address"]["primary"]["mask"]

print("desde XML response ---> " + "GigabitEthernet " + xml_name + " IP:  " + xml_IP + " Mask:  " + xml_Mask)


#to modify values in the dic we can use : xml_response["GigabitEthernet"]["ip"]["address"]["primary"]["address"] = "192.168.0.2" but i need to convert it back xml use unparse
# response_xml = xmltodict.unparse(xml_response)
 
# Now let`s uses RESTCONF to created a loopback interfaces. 

url2 = "https://10.97.4.222:/restconf/data/ietf-interfaces:interfaces"

payload = "{\n    \"ietf-interfaces:interface\": {\n        \"name\": \"Loopback100\",\n        \"description\": \"Configured by RESTCONF\",\n        \"type\": \"iana-if-type:softwareLoopback\",\n        \"enabled\": true,\n        \"ietf-ip:ipv4\": {\n            \"address\": [\n                {\n                    \"ip\": \"172.16.100.1\",\n                    \"netmask\": \"255.255.255.0\"\n                }\n            ]\n        }\n    }\n}"
headers = {
  'Authorization': 'Basic Y2lzY286QzFzY28xMjM0NQ==',
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json'
}

response = requests.request("POST", url2, headers=headers, data = payload, verify=False)

print(response.text.encode('utf8'))


