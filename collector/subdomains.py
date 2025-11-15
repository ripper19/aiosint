import requests

def run(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp =  requests.get(url, timeout=10)
        data =resp.json()
        return [d.get("name_value") for d in data if "name vaue" in d] 
    except Exception as e:
        return {"error": str(e)}
    