    
import requests
import json

from customers.models import Domain

def close_sessions():
    schemas=Domain.objects.all()
    try:
        print("schemas",schemas)
        for domain in schemas:
            print("schema name=",domain.domain)
            domain=domain.domain
            if domain=='public':
                print("public tenant")
                continue
            print("this function runs every 10 seconds")
            url = "http://127.0.0.1:8000/clients/"+domain+"/private/all_session_close/"
            # data = {}
            headers = {'Content-type': 'application/json', 'Accept': '*/*'}
            # r = requests.put(url, data=json.dumps(data), headers=headers, auth=('rzp_test_yourTestApiKey', 'yourTestApiSecret'))
            r = requests.get(url,  headers=headers)
    except Exception as e:
        print("error in close_sessions",e)
        pass
    
    
