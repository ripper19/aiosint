import whois

def run(domain):
    try:
        info = whois.whois(domain)
        return dict(info)
    except Exception as e:
        return {"error" : str (e)}
