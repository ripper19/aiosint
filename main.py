import streamlit as st
from processor import parser
from analyser import ai_analysis
from ui import dash
from storage import db
import whois
from transformers import pipeline

#whois lookup
class whois_lookup:
    def run(domain):
        try:
            info = whois.whois(domain)
            return dict(info)
        except Exception as e:
            return (f"Error {str(e)}")


 #processor//process raw data to clean data that can  be passed to analyzer
class parser:
    def clean(raw_data):
        clean_data= {}
        errored_data = {}

        for key,data in raw_data.items():
            if isinstance(data, dict) and "error" in data:
                errored_data[key] = data["error"]
            else:
                if isinstance(data, dict):
                    clean_data[key] = str(data)
        return clean_data

#ai_anlyser// need to work
"""class ai_analysis:

    summarizer = pipeline("summarizer", model="t5-small")
    categorizer = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

    def get_summary(clean):
        try:
            whois_data = clean.get("whois", {})

            text_parts = []
#domain name - check types
            domain_value = whois_data.get('domain_name')
            if isinstance(domain_value, str) and domain_value.strip():
                    text_parts.append(f"DOmain {domain_value.strip()}")
            elif isinstance(domain_value, list):
                domain_list = [d.strip() for d in domain_value if isinstance(d, str) and d.strip()]
                if domain_list:
                        text_parts.append(f"Domain {domain_list[0]}")
            elif domain_value:
                    text_parts.append(f"Domain {str(domain_value)}")
            
            ##registrar
            registrar = whois_data.get('registrar')
            if registrar:
                text_parts.append(f"Registered by {registrar}")
            
            #creationdate
            created = whois_data.get('cretion_date')
            if created:
                text_parts.append(f"Created on {created}")

            #nameservers
            namevalue = whois_data.get('name_servers')
            if isinstance(namevalue, list):
                 namecount = len([ns for ns in namevalue if ns])
                 if namecount >0:
                      text_parts.append(f"using {namecount} name server{'s' if namecount !=1 else ''}")
            


        except Exception as e:
            return("Error". str(e))

"""


#running main block
def main():
    st.title("AI OSINT Threat intelliJ")


    target = st.text_input("Define target (domain/username: )")

    if st.button("Run Scan") :
        if target.strip():
            st.write(f"\n[+]Gathering OSint for {target}")
            raw_data = {
            "whois": whois_lookup.run(target),
            }#get raw data from whois

        clean_data = parser.clean(raw_data)#clean the data to remove errors

        ai_report = ai_analysis.get_summary(clean_data)
        db.save_result(target, clean_data,ai_report)
        dash.display(target,clean_data,ai_report)
    else:
        st.warning("Fill in")

if __name__ == "__main__":
    main()
