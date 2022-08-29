def ACI_VPC_TRUNK_MODE_PORTS_POST():
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
            ACI_NODE_A_ID = row['ACI_NODE_A_ID']]
            ACI_NODE_B_ID = row['ACI_NODE_B_ID']]
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
                print("The program successfully created/modified/deleted the nonbond access mode port for node , " + ACI_NODE_ID + ", on APIC: " + TARGET_APIC)
                print("\n")
            else:
                print("\n")
                print("The program has run into an issue:, " + TARGET_APIC)
                print("\n")
                print("The APIC, " + TARGET_APIC + ", responded with the status code of " + str(ACI_VPC_TRUNK_MODE_PORTS_POST_CALL.status_code) + ".")
                print(ACI_VPC_TRUNK_MODE_PORTS_POST_CALL.content)
                print("\n")
                exit()
                