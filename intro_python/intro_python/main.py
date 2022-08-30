import requests
import json

#VARIABLES
TARGET_APIC = '10.10.20.14'
USERNAME = 'admin'
PASSWORD = 'C1sco12345'

# Authentication Request
AUTH_URL = "https://" + TARGET_APIC + "/api/aaaLogin.json"
AUTH_PAYLOAD = {
  "aaaUser" : {
    "attributes" : {
      "name" : "" + USERNAME + "",
      "pwd" : "" + PASSWORD + ""
    }
  }
}

print("\n")
print("URL is set too: " + AUTH_URL)
print("\n")
print("JSON is set too: ")
print(json.dumps(AUTH_PAYLOAD, indent=4, sort_keys=True))
print("\n")

AUTH_CALL = requests.post(url=AUTH_URL, json=AUTH_PAYLOAD, verify=False)

# Autentication Response
# Basic Flow Control 
if AUTH_CALL.status_code == 200:
        print("\n")
        print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(AUTH_CALL.status_code) + "")
        print(USERNAME + " has successfully logged into the fabric")
        print("\n")
        
        # VIEW THE RESPONSE
        print("\n")
        print(AUTH_CALL.json())
        print("\n")
        
        # EXTRACT THE TOKEN FROM THE RESPONSE
        JSON_DATA = AUTH_CALL.json()
        ACI_API_TOKEN = JSON_DATA["imdata"][0]["aaaLogin"]["attributes"]["token"]
        HEADERS = {
          "Cookie" : "APIC-Cookie=" + ACI_API_TOKEN + "", 
        }        
        
        print("\n")
        print("Token, " + ACI_API_TOKEN + ", has been extracteed from the authentication response from the APIC.")
        print("\n") 
        
else:
        print("\n")
        print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(AUTH_CALL.status_code) + "")
        print(USERNAME + " HAS NOT successfully logged into the fabric")
        print("\n")
        
        
# Tenant Request
URL = "https://10.10.20.14/api/node/mo/uni/tn-ACI101_PRD_NCI.json"
PAYLOAD = {
  "fvTenant": {
    "attributes": {
      "dn": "uni/tn-ACI101_PRD_NCI",
      "name": "ACI101_PRD_NCI",
      "descr": "ACI 101 Production Network Centric Infrastructure",
      "rn": "tn-ACI101_PRD_NCI",
      "status": "deleted"
    },
    "children": []
  }
}
CALL = requests.post(url=URL, json=PAYLOAD, headers=HEADERS, verify=False)

print("\n")
print("URL is set too: " + URL)
print("\n")
print("JSON is set too: ")
print(json.dumps(PAYLOAD, indent=4, sort_keys=True))
print("\n")

# Tenant Response
if CALL.status_code == 200:
        print("\n")
        print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(CALL.status_code) + "")
        print("The program has successfully created tenant profile, ")
        print("\n")
        
        # VIEW THE RESPONSE
        print("\n")
        print(CALL.json())
        print("\n")
        
else:
        print("\n")
        print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(AUTH_CALL.status_code) + "")
        print("The program HAS NOT successfully created tenant profile, ")
        print("\n")

# VRF Request
URL = "https://10.10.20.14/api/node/mo/uni/tn-ACI101_PRD_NCI/ctx-ACI101_PRD_NCI_DEF_VRF.json"
PAYLOAD = {
  "fvCtx": {
    "attributes": {
      "dn": "uni/tn-ACI101_PRD_NCI/ctx-ACI101_PRD_NCI_DEF_VRF",
      "name": "ACI101_PRD_NCI_DEF_VRF",
      "descr": "ACI 101 Production Network Centric Infrastructure Default Routing Table Virtual Routing & Forwarding",
      "pcEnfPref": "unenforced",
      "rn": "ctx-ACI101_PRD_NCI_DEF_VRF",
      "status": "deleted"
    },
    "children": []
  }
}
CALL = requests.post(url=URL, json=PAYLOAD, headers=HEADERS, verify=False)

print("\n")
print("URL is set too: " + URL)
print("\n")
print("JSON is set too: ")
print(json.dumps(PAYLOAD, indent=4, sort_keys=True))
print("\n")

# VRF Response
if CALL.status_code == 200:
        print("\n")
        print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(CALL.status_code) + "")
        print("The program has successfully created VRF profile, ")
        print("\n")
        
        # VIEW THE RESPONSE
        print("\n")
        print(CALL.json())
        print("\n")
        
else:
        print("\n")
        print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(AUTH_CALL.status_code) + "")
        print("The program HAS NOT successfully created VRF profile, ")
        print("\n")
        
# Bridge Domain Request
URL = "https://10.10.20.14/api/node/mo/uni/tn-ACI101_PRD_NCI/BD-ACI101_PRD_NCI_DATA_VLAN10_BD.json"
PAYLOAD = {
  "fvBD": {
    "attributes": {
      "dn": "uni/tn-ACI101_PRD_NCI/BD-ACI101_PRD_NCI_DATA_VLAN10_BD",
      "mac": "00:22:BD:F8:19:FF",
      "arpFlood": "true",
      "name": "ACI101_PRD_NCI_DATA_VLAN10_BD",
      "descr": "ACI 101 Production Network Centric Infrastructure Data VLAN 10",
      "rn": "BD-ACI101_PRD_NCI_DATA_VLAN10_BD",
      "status": "created"
    },
    "children": [
      {
        "fvSubnet": {
          "attributes": {
            "dn": "uni/tn-ACI101_PRD_NCI/BD-ACI101_PRD_NCI_DATA_VLAN10_BD/subnet-[30.0.10.1/24]",
            "ctrl": "",
            "ip": "30.0.10.1/24",
            "scope": "public",
            "rn": "subnet-[30.0.10.1/24]",
            "status": "created"
          },
          "children": []
        }
      },
      {
        "fvRsCtx": {
          "attributes": {
            "tnFvCtxName": "ACI101_PRD_NCI_DEF_Bridge Domain",
            "status": "created,modified"
          },
          "children": []
        }
      }
    ]
  }
}
CALL = requests.post(url=URL, json=PAYLOAD, headers=HEADERS, verify=False)

print("\n")
print("URL is set too: " + URL)
print("\n")
print("JSON is set too: ")
print(json.dumps(PAYLOAD, indent=4, sort_keys=True))
print("\n")

# Bridge Domain Response
if CALL.status_code == 200:
        print("\n")
        print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(CALL.status_code) + "")
        print("The program has successfully created Bridge Domain profile, ")
        print("\n")
        
        # VIEW THE RESPONSE
        print("\n")
        print(CALL.json())
        print("\n")
        
else:
        print("\n")
        print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(AUTH_CALL.status_code) + "")
        print("The program HAS NOT successfully created Bridge Domain profile, ")
        print("\n")        