import requests
import json
import csv
import os.path
import re

def ACI_LOGIN(TARGET_APIC):
    with open('csv_files/credentials.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            #VARIABLES
            APIC = row['APIC']
            USERNAME = row['USERNAME']
            PASSWORD = row['PASSWORD']
    
            if APIC == TARGET_APIC:
                # REQUEST
                AUTH_URL = 'https://' + APIC + '/api/aaaLogin.json'
                AUTH_PAYLOAD = {"aaaUser":{"attributes":{"name":USERNAME,"pwd":PASSWORD}}}
                AUTH_CALL = requests.post(url=AUTH_URL, json=AUTH_PAYLOAD, verify=False )
                
                # RESPONSE
                if AUTH_CALL.status_code == 200:
                    print("\n")
                    print("The APIC, " + APIC + ", responded with the status code of " + str(AUTH_CALL.status_code) + ".")
                    print(USERNAME + " has successfully logged into the fabric target, " + APIC)
                    print("\n")
                    
                    # Extract the Token
                    JSON_DATA = AUTH_CALL.json()
                    ACI_API_TOKEN = JSON_DATA["imdata"][0]["aaaLogin"]["attributes"]["token"]
                    HEADERS = {
                      "Cookie" : "APIC-Cookie=" + ACI_API_TOKEN + "", 
                    }
                    return HEADERS
                    
                else:
                    print("\n")
                    print("The APIC, " + APIC + ", responded with the status code of " + str(AUTH_CALL.status_code) + ".")
                    print(AUTH_CALL.content)
                    print(USERNAME + " has unsuccessfully logged into the fabric target, " + APIC)
                    print("\n")
                    exit()
    
def ACI_TENANT_POST():
    with open('csv_files/tenants.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_TENANT_POST_NAME = row['TENANT_NAME']
            ACI_TENANT_POST_DESCRIPTION = row['TENANT_DESCRIPTION']
            ACI_TENANT_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_TENANT_POST_URL = 'https://' + TARGET_APIC + '/api/node/mo/uni/tn-' + ACI_TENANT_POST_NAME + '.json'
            ACI_TENANT_POST_JSON = {
                "fvTenant": {
                "attributes": {
                  "dn": "uni/tn-" + ACI_TENANT_POST_NAME + "",
                  "name": ACI_TENANT_POST_NAME,
                  "descr": ACI_TENANT_POST_DESCRIPTION,
                  "rn": ACI_TENANT_POST_NAME,
                  "status": ACI_TENANT_POST_STATE
                },
                "children": []
                }
            }
            print("\n")
            print(ACI_TENANT_POST_URL)
            print("\n")
            print(json.dumps(ACI_TENANT_POST_JSON, indent=4, sort_keys=True))
            print("\n")
            ACI_TENANT_POST_CALL = requests.post(url=ACI_TENANT_POST_URL,json=ACI_TENANT_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_TENANT_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_TENANT_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the tenant, " + ACI_TENANT_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_TENANT_POST_CALL.status_code) + ".")
                print(ACI_TENANT_POST_CALL.content)
                print("\n")
                exit()

def ACI_VRF_POST():
    with open('csv_files/vrfs.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_TENANT_POST_NAME = row['TENANT_NAME']
            ACI_VRF_POST_NAME = row['VRF_NAME']
            ACI_VRF_POST_DESCRIPTION = row['VRF_DESCRIPTION']
            ACI_VRF_POST_ENFORCEMENT = row['VRF_ENFORCEMENT']
            ACI_VRF_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_VRF_POST_URL = 'https://' + TARGET_APIC + '/api/node/mo/uni/tn-' + ACI_TENANT_POST_NAME + '/ctx-' + ACI_VRF_POST_NAME + '.json'
            ACI_VRF_POST_JSON = {
              "fvCtx": {
                "attributes": {
                  "dn": "uni/tn-" + ACI_TENANT_POST_NAME + "/ctx-" + ACI_VRF_POST_NAME + "",
                  "name": "" + ACI_VRF_POST_NAME + "",
                  "descr": "" + ACI_VRF_POST_DESCRIPTION + "",
                  "pcEnfPref": "" + ACI_VRF_POST_ENFORCEMENT + "",
                  "rn": "ctx-" + ACI_VRF_POST_NAME + "",
                  "status": "" + ACI_VRF_POST_STATE + ""
                },
                "children": []
              }
            }
            print("\n")
            print(ACI_VRF_POST_URL)
            print("\n")
            print(json.dumps(ACI_VRF_POST_JSON, indent=4, sort_keys=True))
            print("\n")
            ACI_VRF_POST_CALL = requests.post(url=ACI_VRF_POST_URL,json=ACI_VRF_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_VRF_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VRF_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the VRF, " + ACI_VRF_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VRF_POST_CALL.status_code) + ".")
                print(ACI_VRF_POST_CALL.content)
                print("\n")
                exit()

def ACI_BD_POST():
    with open('csv_files/bridge_domains.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_TENANT_POST_NAME = row['TENANT_NAME']
            ACI_VRF_POST_NAME = row['VRF_NAME']
            ACI_BD_POST_NAME = row['BD_NAME']
            ACI_BD_POST_DESCRIPTION = row['BD_DESCRIPTION']
            ACI_BD_POST_ARPFLOOD = row['arpFlood']
            ACI_BD_POST_SUBNET_GATEWAY = row['SUBNET_GATEWAY']
            ACI_BD_POST_SUBNET_SCOPE = row['SUBNET_SCOPE']
            ACI_BD_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_BD_POST_URL = 'https://' + TARGET_APIC + '/api/node/mo/uni/tn-' + ACI_TENANT_POST_NAME + '/BD-' + ACI_BD_POST_NAME + '.json'
            ACI_BD_POST_JSON = {
              "fvBD": {
                "attributes": {
                  "dn": "uni/tn-" + ACI_TENANT_POST_NAME + "/BD-" + ACI_BD_POST_NAME + "",
                  "arpFlood": "" + ACI_BD_POST_ARPFLOOD + "",
                  "name": "" + ACI_BD_POST_NAME + "",
                  "descr": "" + ACI_BD_POST_DESCRIPTION + "",
                  "rn": "" + ACI_BD_POST_NAME + "",
                  "status": "" + ACI_BD_POST_STATE + ""
                },
                "children": [
                  {
                    "fvSubnet": {
                      "attributes": {
                        "dn": "uni/tn-" + ACI_TENANT_POST_NAME + "/BD-" + ACI_BD_POST_NAME + "/subnet-[" + ACI_BD_POST_SUBNET_GATEWAY + "]",
                        "ctrl": "",
                        "ip": "" + ACI_BD_POST_SUBNET_GATEWAY + "",
                        "scope": "" + ACI_BD_POST_SUBNET_SCOPE + "",
                        "rn": "subnet-[" + ACI_BD_POST_SUBNET_GATEWAY + "]",
                        "status": "" + ACI_BD_POST_STATE + ""
                      },
                      "children": []
                    }
                  },
                  {
                    "fvRsCtx": {
                      "attributes": {
                        "tnFvCtxName": "" + ACI_VRF_POST_NAME + "",
                        "status": "created,modified"
                      },
                      "children": []
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_BD_POST_URL)
            print("\n")
            print(json.dumps(ACI_BD_POST_JSON, indent=4, sort_keys=True))
            print("\n")
            ACI_BD_POST_CALL = requests.post(url=ACI_BD_POST_URL,json=ACI_BD_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_BD_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_BD_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the bridge domain, " + ACI_BD_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_BD_POST_CALL.status_code) + ".")
                print(ACI_BD_POST_CALL.content)
                print("\n")
                exit()

def ACI_AP_POST():
    with open('csv_files/application_profiles.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_TENANT_POST_NAME = row['TENANT_NAME']
            ACI_AP_POST_NAME = row['AP_NAME']
            ACI_AP_POST_DESCRIPTION = row['AP_DESCRIPTION']
            ACI_AP_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_AP_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/tn-" + ACI_TENANT_POST_NAME + "/ap-" + ACI_AP_POST_NAME + ".json"
            ACI_AP_POST_JSON = {
              "fvAp": {
                "attributes": {
                  "dn": "uni/tn-" + ACI_TENANT_POST_NAME + "/ap-" + ACI_AP_POST_NAME + "",
                  "name": "" + ACI_AP_POST_NAME + "",
                  "descr": "" + ACI_AP_POST_DESCRIPTION + "",
                  "rn": "ap-" + ACI_AP_POST_NAME + "",
                  "status": "" + ACI_AP_POST_STATE + ""
                },
                "children": []
              }
            }
            print("\n")
            print(ACI_AP_POST_URL)
            print("\n")
            print(json.dumps(ACI_AP_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_AP_POST_CALL = requests.post(url=ACI_AP_POST_URL,json=ACI_AP_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_AP_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_AP_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the application profile, " + ACI_AP_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_AP_POST_CALL.status_code) + ".")
                print(ACI_AP_POST_CALL.content)
                print("\n")
                exit()

def ACI_aEPG_POST():
    with open('csv_files/application_endpoint_groups.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_TENANT_POST_NAME = row['TENANT_NAME']
            ACI_AP_POST_NAME = row['AP_NAME']
            ACI_aEPG_POST_NAME = row['aEPG_NAME']
            ACI_aEPG_POST_DESCRIPTION = row['aEPG_DESCRIPTION']
            ACI_BD_POST_NAME = row['BD_NAME']
            ACI_aEPG_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_aEPG_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/tn-" + ACI_TENANT_POST_NAME + "/ap-" + ACI_AP_POST_NAME + "/epg-" + ACI_aEPG_POST_NAME + ".json"
            ACI_aEPG_POST_JSON = {
              "fvAEPg": {
                "attributes": {
                  "dn": "uni/tn-" + ACI_TENANT_POST_NAME + "/ap-" + ACI_AP_POST_NAME + "/epg-" + ACI_aEPG_POST_NAME + "",
                  "prio": "level3",
                  "name": "" + ACI_aEPG_POST_NAME + "",
                  "descr": "" + ACI_aEPG_POST_DESCRIPTION + "",
                  "rn": "epg-" + ACI_aEPG_POST_NAME + "",
                  "status": "" + ACI_aEPG_POST_STATE + ""
                },
                "children": [
                  {
                    "fvRsBd": {
                      "attributes": {
                        "tnFvBDName": "" + ACI_BD_POST_NAME + "",
                        "status": "created,modified"
                      },
                      "children": []
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_aEPG_POST_URL)
            print("\n")
            print(json.dumps(ACI_aEPG_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_aEPG_POST_CALL = requests.post(url=ACI_aEPG_POST_URL,json=ACI_aEPG_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_aEPG_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_aEPG_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the application endpoint group, " + ACI_aEPG_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_aEPG_POST_CALL.status_code) + ".")
                print(ACI_aEPG_POST_CALL.content)
                print("\n")
                exit()

def ACI_SW_PROFILE_POST_POST():
    with open('csv_files/switch_profiles.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_SW_PROFILE_POST_NAME = row['SW_PROFILE_NAME']
            ACI_SW_PROFILE_POST_DESCRIPTION = row['SW_PROFILE_DESCRIPTION']
            ACI_SW_PROFILE_POST_NODE_ID_FROM = row['SW_PROFILE_NODE_ID_FROM']
            ACI_SW_PROFILE_POST_NODE_ID_TO = row['SW_PROFILE_NODE_ID_TO']
            ACI_SW_PROFILE_POST_SW_NAME = row['SW_NAME']
            ACI_SW_PROFILE_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_SW_PROFILE_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/infra/nprof-" + ACI_SW_PROFILE_POST_NAME + ".json"
            ACI_SW_PROFILE_POST_JSON = {
              "infraNodeP": {
                "attributes": {
                  "dn": "uni/infra/nprof-" + ACI_SW_PROFILE_POST_NAME + "",
                  "name": "" + ACI_SW_PROFILE_POST_NAME + "",
                  "descr": "" + ACI_SW_PROFILE_POST_DESCRIPTION + "",
                  "rn": "nprof-" + ACI_SW_PROFILE_POST_NAME + "",
                  "status": "" + ACI_SW_PROFILE_POST_STATE + ""
                },
                "children": [
                  {
                    "infraLeafS": {
                      "attributes": {
                        "dn": "uni/infra/nprof-" + ACI_SW_PROFILE_POST_NAME + "/leaves-" + ACI_SW_PROFILE_POST_SW_NAME + "-typ-range",
                        "type": "range",
                        "name": "" + ACI_SW_PROFILE_POST_SW_NAME + "",
                        "rn": "leaves-" + ACI_SW_PROFILE_POST_SW_NAME + "-typ-range",
                        "status": "created"
                      },
                      "children": [
                        {
                          "infraNodeBlk": {
                            "attributes": {
                              "dn": "uni/infra/nprof-" + ACI_SW_PROFILE_POST_NAME + "/leaves-" + ACI_SW_PROFILE_POST_SW_NAME + "-typ-range/nodeblk-cbd6cea1fa6052b6",
                              "from_": "" + ACI_SW_PROFILE_POST_NODE_ID_FROM + "",
                              "to_": "" + ACI_SW_PROFILE_POST_NODE_ID_TO + "",
                              "name": "cbd6cea1fa6052b6",
                              "rn": "nodeblk-cbd6cea1fa6052b6",
                              "status": "created"
                            },
                            "children": []
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_SW_PROFILE_POST_URL)
            print("\n")
            print(json.dumps(ACI_SW_PROFILE_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_SW_PROFILE_POST_CALL = requests.post(url=ACI_SW_PROFILE_POST_URL,json=ACI_SW_PROFILE_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_SW_PROFILE_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_SW_PROFILE_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the switch profile, " + ACI_SW_PROFILE_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_SW_PROFILE_POST_CALL.status_code) + ".")
                print(ACI_SW_PROFILE_POST_CALL.content)
                print("\n")
                exit()

def ACI_AAEP_POST():
    with open('csv_files/attachable_access_entity_profiles.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_AAEP_POST_NAME = row['AAEP_NAME']
            ACI_AAEP_POST_DESCRIPTION = row['AAEP_DESCRIPTION']
            ACI_AAEP_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_AAEP_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/infra.json"
            ACI_AAEP_POST_JSON = {
              "infraInfra": {
                "attributes": {
                  "dn": "uni/infra",
                  "status": "modified"
                },
                "children": [
                  {
                    "infraAttEntityP": {
                      "attributes": {
                        "dn": "uni/infra/attentp-" + ACI_AAEP_POST_NAME + "",
                        "descr": "" + ACI_AAEP_POST_DESCRIPTION + "",
                        "name": "" + ACI_AAEP_POST_NAME + "",
                        "rn": "attentp-" + ACI_AAEP_POST_NAME + "",
                        "status": "" + ACI_AAEP_POST_STATE + ""
                      },
                      "children": []
                    }
                  },
                  {
                    "infraFuncP": {
                      "attributes": {
                        "dn": "uni/infra/funcprof",
                        "status": "modified"
                      },
                      "children": []
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_AAEP_POST_URL)
            print("\n")
            print(json.dumps(ACI_AAEP_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_AAEP_POST_CALL = requests.post(url=ACI_AAEP_POST_URL,json=ACI_AAEP_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_AAEP_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_AAEP_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the attachable access entity profile, " + ACI_AAEP_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_AAEP_POST_CALL.status_code) + ".")
                print(ACI_AAEP_POST_CALL.content)
                print("\n")
                exit()

def ACI_VLAN_POOL_POST():
    with open('csv_files/vlan_pools.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_VLAN_POOL_POST_NAME = row['VLAN_POOL_NAME']
            ACI_VLAN_POOL_POST_DESCRIPTION = row['VLAN_POOL_DESCRIPTION']
            ACI_VLAN_POOL_POST_VLAN_FROM = row['VLAN_ID_FROM']
            ACI_VLAN_POOL_POST_VLAN_TO = row['VLAN_ID_TO']
            ACI_VLAN_POOL_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_VLAN_POOL_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/infra/vlanns-[" + ACI_VLAN_POOL_POST_NAME + "]-static.json"
            ACI_VLAN_POOL_POST_JSON = {
              "fvnsVlanInstP": {
                "attributes": {
                  "dn": "uni/infra/vlanns-[" + ACI_VLAN_POOL_POST_NAME + "]-static",
                  "descr": "" + ACI_VLAN_POOL_POST_DESCRIPTION + "",
                  "name": "" + ACI_VLAN_POOL_POST_NAME + "",
                  "allocMode": "static",
                  "rn": "vlanns-[" + ACI_VLAN_POOL_POST_NAME + "]-static",
                  "status": "" + ACI_VLAN_POOL_POST_STATE + ""
                },
                "children": [
                  {
                    "fvnsEncapBlk": {
                      "attributes": {
                        "dn": "uni/infra/vlanns-[" + ACI_VLAN_POOL_POST_NAME + "]-static/from-[vlan-" + ACI_VLAN_POOL_POST_VLAN_FROM + "]-to-[vlan-" + ACI_VLAN_POOL_POST_VLAN_TO + "]",
                        "from": "vlan-" + ACI_VLAN_POOL_POST_VLAN_FROM + "",
                        "to": "vlan-" + ACI_VLAN_POOL_POST_VLAN_TO + "",
                        "allocMode": "static",
                        "rn": "from-[vlan-" + ACI_VLAN_POOL_POST_VLAN_FROM + "]-to-[vlan-" + ACI_VLAN_POOL_POST_VLAN_TO + "]",
                        "status": "created"
                      },
                      "children": []
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_VLAN_POOL_POST_URL)
            print("\n")
            print(json.dumps(ACI_VLAN_POOL_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_VLAN_POOL_POST_CALL = requests.post(url=ACI_VLAN_POOL_POST_URL,json=ACI_VLAN_POOL_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_VLAN_POOL_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VLAN_POOL_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the VLAN POOL, " + ACI_VLAN_POOL_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VLAN_POOL_POST_CALL.status_code) + ".")
                print(ACI_VLAN_POOL_POST_CALL.content)
                print("\n")
                exit()

def ACI_PHYS_DOM_POST():
    with open('csv_files/physical_domains.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_VLAN_POOL_POST_NAME = row['VLAN_POOL_NAME']
            ACI_PHYS_DOM_POST_NAME = row['PHYSICAL_DOMAIN_NAME']
            ACI_PHYS_DOM_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_PHYS_DOM_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/phys-" + ACI_PHYS_DOM_POST_NAME + ".json"
            ACI_PHYS_DOM_POST_JSON = {
              "physDomP": {
                "attributes": {
                  "dn": "uni/phys-" + ACI_PHYS_DOM_POST_NAME + "",
                  "name": "" + ACI_PHYS_DOM_POST_NAME + "",
                  "rn": "phys-" + ACI_PHYS_DOM_POST_NAME + "",
                  "status": "" + ACI_PHYS_DOM_POST_STATE + ""
                },
                "children": [
                  {
                    "infraRsVlanNs": {
                      "attributes": {
                        "tDn": "uni/infra/vlanns-[" + ACI_VLAN_POOL_POST_NAME + "]-static",
                        "status": "created"
                      },
                      "children": []
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_PHYS_DOM_POST_URL)
            print("\n")
            print(json.dumps(ACI_PHYS_DOM_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_PHYS_DOM_POST_CALL = requests.post(url=ACI_PHYS_DOM_POST_URL,json=ACI_PHYS_DOM_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_PHYS_DOM_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_PHYS_DOM_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the PHYSICAL DOMAIN, " + ACI_PHYS_DOM_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_PHYS_DOM_POST_CALL.status_code) + ".")
                print(ACI_PHYS_DOM_POST_CALL.content)
                print("\n")
                exit()

def ACI_INT_PROF_POST():
    with open('csv_files/interface_profiles.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_INT_PROF_POST_NAME = row['INT_PROF_NAME']
            ACI_INT_PROF_POST_DESCRIPTION = row['INT_PROF_DESCRIPTION']
            ACI_INT_PROF_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_INT_PROF_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/infra/accportprof-" + ACI_INT_PROF_POST_NAME + ".json"
            ACI_INT_PROF_POST_JSON = {
              "infraAccPortP": {
                "attributes": {
                  "dn": "uni/infra/accportprof-" + ACI_INT_PROF_POST_NAME + "",
                  "descr": "" + ACI_INT_PROF_POST_DESCRIPTION + "",
                  "name": "" + ACI_INT_PROF_POST_NAME + "",
                  "rn": "accportprof-" + ACI_INT_PROF_POST_NAME + "",
                  "status": "" + ACI_INT_PROF_POST_STATE + ""
                },
                "children": []
              }
            }
            print("\n")
            print(ACI_INT_PROF_POST_URL)
            print("\n")
            print(json.dumps(ACI_INT_PROF_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_INT_PROF_POST_CALL = requests.post(url=ACI_INT_PROF_POST_URL,json=ACI_INT_PROF_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_INT_PROF_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_INT_PROF_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the interface profile, " + ACI_INT_PROF_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_INT_PROF_POST_CALL.status_code) + ".")
                print(ACI_INT_PROF_POST_CALL.content)
                print("\n")
                exit()
                
def ACI_NB_INT_POL_POST():
    with open('csv_files/nonbond_interface_policies.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_AAEP_POST_NAME = row['AAEP_NAME']
            ACI_NB_INT_POL_POST_NAME = row['INT_POL_NAME']
            ACI_NB_INT_POL_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_NB_INT_POL_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/infra/funcprof/accportgrp-" + ACI_NB_INT_POL_POST_NAME + ".json"
            ACI_NB_INT_POL_POST_JSON = {
              "infraAccPortGrp": {
                "attributes": {
                  "dn": "uni/infra/funcprof/accportgrp-" + ACI_NB_INT_POL_POST_NAME + "",
                  "name": "" + ACI_NB_INT_POL_POST_NAME + "",
                  "rn": "accportgrp-" + ACI_NB_INT_POL_POST_NAME + "",
                  "status": "" + ACI_NB_INT_POL_POST_STATE + ""
                },
                "children": [
                  {
                    "infraRsAttEntP": {
                      "attributes": {
                        "tDn": "uni/infra/attentp-" + ACI_AAEP_POST_NAME + "",
                        "status": "created,modified"
                      },
                      "children": []
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_NB_INT_POL_POST_URL)
            print("\n")
            print(json.dumps(ACI_NB_INT_POL_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_NB_INT_POL_POST_CALL = requests.post(url=ACI_NB_INT_POL_POST_URL,json=ACI_NB_INT_POL_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_NB_INT_POL_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_NB_INT_POL_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the interface policy, " + ACI_NB_INT_POL_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_NB_INT_POL_POST_CALL.status_code) + ".")
                print(ACI_NB_INT_POL_POST_CALL.content)
                print("\n")
                exit()

def ACI_VPC_INT_POL_POST():
    with open('csv_files/vpc_interface_policies.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_AAEP_POST_NAME = row['AAEP_NAME']
            ACI_VPC_INT_POL_POST_NAME = row['INT_POL_NAME']
            ACI_VPC_INT_POL_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_VPC_INT_POL_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/infra/funcprof/accbundle-" + ACI_VPC_INT_POL_POST_NAME + ".json"
            ACI_VPC_INT_POL_POST_JSON = {
              "infraAccBndlGrp": {
                "attributes": {
                  "dn": "uni/infra/funcprof/accbundle-" + ACI_VPC_INT_POL_POST_NAME + "",
                  "lagT": "node",
                  "name": "" + ACI_VPC_INT_POL_POST_NAME + "",
                  "rn": "accbundle-" + ACI_VPC_INT_POL_POST_NAME + "",
                  "status": "" + ACI_VPC_INT_POL_POST_STATE + ""
                },
                "children": [
                  {
                    "infraRsAttEntP": {
                      "attributes": {
                        "tDn": "uni/infra/attentp-" + ACI_AAEP_POST_NAME + "",
                        "status": "created,modified"
                      },
                      "children": []
                    }
                  },
                  {
                    "infraRsLacpPol": {
                      "attributes": {
                        "tnLacpLagPolName": "lacp_active",
                        "status": "created,modified"
                      },
                      "children": []
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_VPC_INT_POL_POST_URL)
            print("\n")
            print(json.dumps(ACI_VPC_INT_POL_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_VPC_INT_POL_POST_CALL = requests.post(url=ACI_VPC_INT_POL_POST_URL,json=ACI_VPC_INT_POL_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_VPC_INT_POL_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VPC_INT_POL_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the interface policy, " + ACI_VPC_INT_POL_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VPC_INT_POL_POST_CALL.status_code) + ".")
                print(ACI_VPC_INT_POL_POST_CALL.content)
                print("\n")
                exit()

def ACI_INT_SELECTOR_POST():
    with open('csv_files/interface_selectors.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_INT_PROF_POST_NAME = row['INT_PROF_NAME']
            ACI_INT_SELECTOR_POST_NAME = row['INT_SELECTOR_NAME']
            ACI_INT_SELECTOR_POST_PORT_FROM = row['INT_FROM']
            ACI_INT_SELECTOR_POST_PORT_TO = row['INT_TO']
            ACI_INT_POL_POST_NAME = row['INT_POL_NAME']
            ACI_INT_SELECTOR_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_INT_SELECTOR_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/infra/accportprof-" + ACI_INT_PROF_POST_NAME + "/hports-" + ACI_INT_SELECTOR_POST_NAME + "-typ-range.json"
            ACI_INT_SELECTOR_POST_JSON = {
              "infraHPortS": {
                "attributes": {
                  "dn": "uni/infra/accportprof-" + ACI_INT_PROF_POST_NAME + "/hports-" + ACI_INT_SELECTOR_POST_NAME + "-typ-range",
                  "name": "" + ACI_INT_SELECTOR_POST_NAME + "",
                  "rn": "hports-" + ACI_INT_SELECTOR_POST_NAME + "-typ-range",
                  "status": "" + ACI_INT_SELECTOR_POST_STATE + ""
                },
                "children": [
                  {
                    "infraPortBlk": {
                      "attributes": {
                        "dn": "uni/infra/accportprof-" + ACI_INT_PROF_POST_NAME + "/hports-" + ACI_INT_SELECTOR_POST_NAME + "-typ-range/portblk-block2",
                        "fromPort": "" + ACI_INT_SELECTOR_POST_PORT_FROM + "",
                        "toPort": "" + ACI_INT_SELECTOR_POST_PORT_TO + "",                        
                        "name": "block2",
                        "rn": "portblk-block2",
                        "status": "created,modified"
                      },
                      "children": []
                    }
                  },
                  {
                    "infraRsAccBaseGrp": {
                      "attributes": {
                        "tDn": "uni/infra/funcprof/accbundle-" + ACI_INT_POL_POST_NAME + "",
                        "status": "created,modified"
                      },
                      "children": []
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_INT_SELECTOR_POST_URL)
            print("\n")
            print(json.dumps(ACI_INT_SELECTOR_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_INT_SELECTOR_POST_CALL = requests.post(url=ACI_INT_SELECTOR_POST_URL,json=ACI_INT_SELECTOR_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_INT_SELECTOR_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_INT_SELECTOR_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the interface selector, " + ACI_INT_SELECTOR_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_INT_SELECTOR_POST_CALL.status_code) + ".")
                print(ACI_INT_SELECTOR_POST_CALL.content)
                print("\n")
                exit()

def ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST():
    with open('csv_files/associate_aEPGs_to_physical_domains.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_TENANT_POST_NAME = row['TENANT_NAME']
            ACI_AP_POST_NAME = row['AP_NAME']
            ACI_aEPG_POST_NAME = row['aEPG_NAME']
            ACI_PHYS_DOM_POST_NAME = row['PHYSICAL_DOMAIN_NAME']
            ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/tn-" + ACI_TENANT_POST_NAME + "/ap-" + ACI_AP_POST_NAME + "/epg-" + ACI_aEPG_POST_NAME + ".json"
            ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_JSON = {
              "fvRsDomAtt": {
                "attributes": {
                  "resImedcy": "immediate",
                  "tDn": "uni/phys-" + ACI_PHYS_DOM_POST_NAME + "",
                  "status": "" + ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_STATE + ""
                },
                "children": []
              }
            }
            print("\n")
            print(ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_URL)
            print("\n")
            print(json.dumps(ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_CALL = requests.post(url=ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_URL,json=ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_CALL.status_code) + ".")
                print("The program successfully associated the aEPG, " + ACI_aEPG_POST_NAME + ", to physical domain, " + ACI_PHYS_DOM_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_CALL.status_code) + ".")
                print(ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST_CALL.content)
                print("\n")
                exit()

def ACI_NONBOND_ACCESS_MODE_PORTS_POST():
    with open('csv_files/nonbond_access_mode_ports.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_TENANT_POST_NAME = row['TENANT_NAME']
            ACI_AP_POST_NAME = row['AP_NAME']
            ACI_aEPG_POST_NAME = row['aEPG_NAME']
            ACI_aEPG_POST_VLAN_ID = row['aEPG_VLAN_ID']
            ACI_POD_NUMBER = row['ACI_POD_NUMBER']
            ACI_NODE_ID = row['ACI_NODE_ID']
            ACI_NODE_SLOT = row['ACI_NODE_SLOT']
            ACI_NODE_PORT = row['ACI_NODE_PORT']
            ACI_NONBOND_ACCESS_MODE_PORTS_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_NONBOND_ACCESS_MODE_PORTS_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/tn-" + ACI_TENANT_POST_NAME + "/ap-" + ACI_AP_POST_NAME + "/epg-" + ACI_aEPG_POST_NAME + "/rspathAtt-[topology/pod-" + ACI_POD_NUMBER + "/paths-" + ACI_NODE_ID + "/pathep-[eth" + ACI_NODE_SLOT + "/" + ACI_NODE_PORT + "]].json"
            ACI_NONBOND_ACCESS_MODE_PORTS_POST_JSON = {
              "fvRsPathAtt": {
                "attributes": {
                  "dn": "uni/tn-" + ACI_TENANT_POST_NAME + "/ap-" + ACI_AP_POST_NAME + "/epg-" + ACI_aEPG_POST_NAME + "/rspathAtt-[topology/pod-" + ACI_POD_NUMBER + "/paths-" + ACI_NODE_ID + "/pathep-[eth" + ACI_NODE_SLOT + "/" + ACI_NODE_PORT + "]]",
                  "encap": "vlan-" + ACI_aEPG_POST_VLAN_ID + "",
                  "instrImedcy": "immediate",
                  "mode": "native",
                  "tDn": "topology/pod-" + ACI_POD_NUMBER + "/paths-" + ACI_NODE_ID + "/pathep-[eth" + ACI_NODE_SLOT + "/" + ACI_NODE_PORT + "]",
                  "rn": "rspathAtt-[topology/pod-" + ACI_POD_NUMBER + "/paths-" + ACI_NODE_ID + "/pathep-[eth" + ACI_NODE_SLOT + "/" + ACI_NODE_PORT + "]]",
                  "status": "" + ACI_NONBOND_ACCESS_MODE_PORTS_POST_STATE + ""
                },
                "children": []
              }
            }
            print("\n")
            print(ACI_NONBOND_ACCESS_MODE_PORTS_POST_URL)
            print("\n")
            print(json.dumps(ACI_NONBOND_ACCESS_MODE_PORTS_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_NONBOND_ACCESS_MODE_PORTS_POST_CALL = requests.post(url=ACI_NONBOND_ACCESS_MODE_PORTS_POST_URL,json=ACI_NONBOND_ACCESS_MODE_PORTS_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_NONBOND_ACCESS_MODE_PORTS_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_NONBOND_ACCESS_MODE_PORTS_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the nonbond access mode port for node , " + ACI_NODE_ID + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_NONBOND_ACCESS_MODE_PORTS_POST_CALL.status_code) + ".")
                print(ACI_NONBOND_ACCESS_MODE_PORTS_POST_CALL.content)
                print("\n")
                exit()

def ACI_VPC_TRUNK_MODE_PORTS_POST():
    with open('csv_files/vpc_trunk_mode_ports.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_TENANT_POST_NAME = row['TENANT_NAME']
            ACI_AP_POST_NAME = row['AP_NAME']
            ACI_aEPG_POST_NAME = row['aEPG_NAME']
            ACI_aEPG_POST_VLAN_ID = row['aEPG_VLAN_ID']
            ACI_POD_NUMBER = row['ACI_POD_NUMBER']
            ACI_NODE_A_ID = row['ACI_NODE_A_ID']
            ACI_NODE_B_ID = row['ACI_NODE_B_ID']
            ACI_VPC_INT_POL_POST_NAME = row['VPC_INT_POL_NAME']
            ACI_VPC_TRUNK_MODE_PORTS_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_VPC_TRUNK_MODE_PORTS_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/tn-" + ACI_TENANT_POST_NAME + "/ap-" + ACI_AP_POST_NAME + "/epg-" + ACI_aEPG_POST_NAME + "/rspathAtt-[topology/pod-" + ACI_POD_NUMBER + "/protpaths-" + ACI_NODE_A_ID + "-" + ACI_NODE_B_ID + "/pathep-[" + ACI_VPC_INT_POL_POST_NAME + "]].json"
            ACI_VPC_TRUNK_MODE_PORTS_POST_JSON = {
              "fvRsPathAtt": {
                "attributes": {
                  "encap": "vlan-" + ACI_aEPG_POST_VLAN_ID + "",
                  "instrImedcy": "immediate",
                  "tDn": "topology/pod-" + ACI_POD_NUMBER + "/protpaths-" + ACI_NODE_A_ID + "-" + ACI_NODE_B_ID + "/pathep-[" + ACI_VPC_INT_POL_POST_NAME + "]",
                  "status": "" + ACI_VPC_TRUNK_MODE_PORTS_POST_STATE + ""
                },
                "children": []
              }
            }
            print("\n")
            print(ACI_VPC_TRUNK_MODE_PORTS_POST_URL)
            print("\n")
            print(json.dumps(ACI_VPC_TRUNK_MODE_PORTS_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_VPC_TRUNK_MODE_PORTS_POST_CALL = requests.post(url=ACI_VPC_TRUNK_MODE_PORTS_POST_URL,json=ACI_VPC_TRUNK_MODE_PORTS_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_VPC_TRUNK_MODE_PORTS_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VPC_TRUNK_MODE_PORTS_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the vpc trunk mode port for nodes , " + ACI_NODE_A_ID + "-" + ACI_NODE_B_ID + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VPC_TRUNK_MODE_PORTS_POST_CALL.status_code) + ".")
                print(ACI_VPC_TRUNK_MODE_PORTS_POST_CALL.content)
                print("\n")
                exit()

def ACI_VPC_DOMAIN_ID_POST():
    with open('csv_files/vpc_domain_ids.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_VPC_DOMAIN_ID_POST_NAME = row['VPC_DOMAIN_ID_NAME']
            ACI_VPC_DOMAIN_ID_POST_NUMBER = row['VPC_DOMAIN_ID_NUMBER']
            ACI_VPC_DOMAIN_ID_POST_NODE_A = row['VPC_DOMAIN_ID_NODE_A']
            ACI_VPC_DOMAIN_ID_POST_NODE_B = row['VPC_DOMAIN_ID_NODE_B']
            ACI_VPC_DOMAIN_ID_POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_VPC_DOMAIN_ID_POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/fabric/protpol/expgep-" + ACI_VPC_DOMAIN_ID_POST_NAME + ".json"
            ACI_VPC_DOMAIN_ID_POST_JSON = {
              "fabricExplicitGEp": {
                "attributes": {
                  "dn": "uni/fabric/protpol/expgep-" + ACI_VPC_DOMAIN_ID_POST_NAME + "",
                  "name": "" + ACI_VPC_DOMAIN_ID_POST_NAME + "",
                  "id": "" + ACI_VPC_DOMAIN_ID_POST_NUMBER + "",
                  "rn": "expgep-" + ACI_VPC_DOMAIN_ID_POST_NAME + "",
                  "status": "" + ACI_VPC_DOMAIN_ID_POST_STATE + ""
                },
                "children": [
                  {
                    "fabricNodePEp": {
                      "attributes": {
                        "dn": "uni/fabric/protpol/expgep-" + ACI_VPC_DOMAIN_ID_POST_NAME + "/nodepep-" + ACI_VPC_DOMAIN_ID_POST_NODE_A + "",
                        "id": "" + ACI_VPC_DOMAIN_ID_POST_NODE_A + "",
                        "status": "created",
                        "rn": "nodepep-" + ACI_VPC_DOMAIN_ID_POST_NODE_A + ""
                      },
                      "children": []
                    }
                  },
                  {
                    "fabricNodePEp": {
                      "attributes": {
                        "dn": "uni/fabric/protpol/expgep-" + ACI_VPC_DOMAIN_ID_POST_NAME + "/nodepep-" + ACI_VPC_DOMAIN_ID_POST_NODE_B + "",
                        "id": "" + ACI_VPC_DOMAIN_ID_POST_NODE_B + "",
                        "status": "created",
                        "rn": "nodepep-" + ACI_VPC_DOMAIN_ID_POST_NODE_B + ""
                      },
                      "children": []
                    }
                  },
                  {
                    "fabricRsVpcInstPol": {
                      "attributes": {
                        "tnVpcInstPolName": "default",
                        "status": "created,modified"
                      },
                      "children": []
                    }
                  }
                ]
              }
            }
            print("\n")
            print(ACI_VPC_DOMAIN_ID_POST_URL)
            print("\n")
            print(json.dumps(ACI_VPC_DOMAIN_ID_POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_VPC_DOMAIN_ID_POST_CALL = requests.post(url=ACI_VPC_DOMAIN_ID_POST_URL,json=ACI_VPC_DOMAIN_ID_POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_VPC_DOMAIN_ID_POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VPC_DOMAIN_ID_POST_CALL.status_code) + ".")
                print("The program successfully created/modified/deleted the vpc domain id , " + ACI_VPC_DOMAIN_ID_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VPC_DOMAIN_ID_POST_CALL.status_code) + ".")
                print(ACI_VPC_DOMAIN_ID_POST_CALL.content)
                print("\n")
                exit()
  
def ACI_ASSOCIATE_SW_INT_PROFILES__POST():
    with open('csv_files/associate_SW_INT_profiles.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            
            # VARIABLES
            TARGET_APIC = row['TARGET_APIC']
            ACI_SW_PROFILE_POST_NAME = row['SW_PROFILE_NAME']
            ACI_INT_PROF_POST_NAME = row['INT_PROF_NAME']
            ACI_ASSOCIATE_SW_INT_PROFILES__POST_STATE = row['STATE']
            HEADERS = ACI_LOGIN(TARGET_APIC)

            # REQUEST
            ACI_ASSOCIATE_SW_INT_PROFILES__POST_URL = "https://" + TARGET_APIC + "/api/node/mo/uni/infra/nprof-" + ACI_SW_PROFILE_POST_NAME + ".json"
            ACI_ASSOCIATE_SW_INT_PROFILES__POST_JSON = {
              "infraRsAccPortP": {
                "attributes": {
                  "tDn": "uni/infra/accportprof-" + ACI_INT_PROF_POST_NAME + "",
                  "status": "created,modified"
                },
                "children": []
              }
            }
            print("\n")
            print(ACI_ASSOCIATE_SW_INT_PROFILES__POST_URL)
            print("\n")
            print(json.dumps(ACI_ASSOCIATE_SW_INT_PROFILES__POST_JSON, indent=4, sort_keys=True))
            print("\n")            
            ACI_ASSOCIATE_SW_INT_PROFILES__POST_CALL = requests.post(url=ACI_ASSOCIATE_SW_INT_PROFILES__POST_URL,json=ACI_ASSOCIATE_SW_INT_PROFILES__POST_JSON,headers=HEADERS,verify=False)
            
            # RESPONSE
            if ACI_ASSOCIATE_SW_INT_PROFILES__POST_CALL.status_code == 200:
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_ASSOCIATE_SW_INT_PROFILES__POST_CALL.status_code) + ".")
                print("The program successfully associated " + ACI_INT_PROF_POST_NAME + " with " + ACI_SW_PROFILE_POST_NAME + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_ASSOCIATE_SW_INT_PROFILES__POST_CALL.status_code) + ".")
                print(ACI_ASSOCIATE_SW_INT_PROFILES__POST_CALL.content)
                print("\n")
                exit()
                  
                
while True:
    print('Author: Trevor Patch')
    print('Release Date: 08/24/2022')
    print('Script Version: 1')
    print('APIC Version 5.2')
    
    print('\n')
    print('--------------------------------')
    print('\n')
    
    print('Menu: ')
    print('0. Quit')
    print('1. Build/Delete ACI 101 Lab Scenario')
    print('2. Tenant Collection - Create/Modify/Delete')
    print('3. VRF Collection - Create/Modify/Delete')
    print('4. Bridge Domains (Unicast On) Collection - Create/Modify/Delete')
    print('5. Application Profiles Collection - Create/Modify/Delete')
    print('6. Application Endpoint Group Collection - Create/Modify/Delete')
    print('7. Switch Profiles Collection - Create/Modify/Delete')
    print('8. Attachable Access Entity Profile - Create/Modify/Delete')
    print('9. VLAN Pools - Create/Modify/Delete')
    print('10. Physical Domain - Create/Modify/Delete')
    print('11. Interface Profiles - Create/Modify/Delete')
    print('12. Nonbond Interface Policy - Create/Modify/Delete')
    print('13. VPC Interface Policy - Create/Modify/Delete')
    print('14. Interface Selectors - Create/Modify/Delete')
    print('15. Associate aEPG to Physical Domain - Create/Modify/Delete')
    print('16. Associate Switch and Interface Profiles - Create/Modify/Delete')    
    print('17. VPC Domain IDs - Create/Modify/Delete')     
    print('18. aEPG Static Binding, nonbond access mode port - Create/Modify/Delete') 
    print('19. aEPG Static Binding, vpc trunk mode port - Create/Modify/Delete')
    
    MENU_SELECTION = input("PLEASE SELECT A MENU NUMBER: ")
    
    if MENU_SELECTION == 0:
        break
    elif MENU_SELECTION == 1:
        ACI_TENANT_POST()
        ACI_VRF_POST()
        ACI_BD_POST()
        ACI_AP_POST()
        ACI_aEPG_POST()
        ACI_SW_PROFILE_POST_POST()
        ACI_AAEP_POST()
        ACI_VLAN_POOL_POST()
        ACI_PHYS_DOM_POST()
        ACI_INT_PROF_POST()
        ACI_NB_INT_POL_POST()
        ACI_VPC_INT_POL_POST()
        ACI_INT_SELECTOR_POST()
        ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST()
        ACI_ASSOCIATE_SW_INT_PROFILES__POST()
        ACI_VPC_DOMAIN_ID_POST()
        ACI_NONBOND_ACCESS_MODE_PORTS_POST()
        ACI_VPC_TRUNK_MODE_PORTS_POST()
    elif MENU_SELECTION == 2:
        ACI_TENANT_POST()
    elif MENU_SELECTION == 3:
        ACI_VRF_POST()
    elif MENU_SELECTION == 4:
        ACI_BD_POST()
    elif MENU_SELECTION == 5:
        ACI_AP_POST()
    elif MENU_SELECTION == 6:
        ACI_aEPG_POST() 
    elif MENU_SELECTION == 7:
        ACI_SW_PROFILE_POST_POST()
    elif MENU_SELECTION == 8:
        ACI_AAEP_POST()
    elif MENU_SELECTION == 9:
        ACI_VLAN_POOL_POST()   
    elif MENU_SELECTION == 10:
        ACI_PHYS_DOM_POST()
    elif MENU_SELECTION == 11:
        ACI_INT_PROF_POST()  
    elif MENU_SELECTION == 12:
        ACI_NB_INT_POL_POST()    
    elif MENU_SELECTION == 13:
        ACI_VPC_INT_POL_POST()     
    elif MENU_SELECTION == 14:
        ACI_INT_SELECTOR_POST()    
    elif MENU_SELECTION == 15:
        ACI_ASSOCIATE_aEPG_PHYSDOMAIN_POST()
    elif MENU_SELECTION == 16:
        ACI_ASSOCIATE_SW_INT_PROFILES__POST()        
    elif MENU_SELECTION == 17:
        ACI_VPC_DOMAIN_ID_POST()         
    elif MENU_SELECTION == 18:
        ACI_NONBOND_ACCESS_MODE_PORTS_POST()
    elif MENU_SELECTION == 19:
        ACI_VPC_TRUNK_MODE_PORTS_POST()          
    else:
        print('Invalid Menu Selection. Please input the menu number only.')