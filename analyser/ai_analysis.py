from transformers import pipeline
import json

summarizer = pipeline("summarization", model="t5-small")
categorizer = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

def get_summary(clean_data):
    try:
        # Create a very structured input
        whois_data = clean_data.get('whois', {})
        
        # Build structured text
        text_parts = []
        if whois_data.get('domain_name'):
            text_parts.append(f"Domain {whois_data['domain_name']}")
        if whois_data.get('registrar'):
            text_parts.append(f"registered with {whois_data['registrar']}")
        if whois_data.get('creation_date'):
            text_parts.append(f"created on {whois_data['creation_date']}")

        if whois_data.get('name_servers'):
            ns_count = len(whois_data['name_servers'])

            text_parts.append(f"using {ns_count} name servers")
            
        if whois_data.get('country'):
            text_parts.append(f"based in {whois_data['country']}")
            
        text = ". ".join(text_parts) + "."
        
        if len(text) < 50:  # If too short, use fallback
            return fallback_report(clean_data)
        
        # Summarize
        summary = summarizer(
            text, 
            max_length=80,
            min_length=20,
            do_sample=False,
            truncation=True
        )[0]['summary_text']
        
        # Risk assessment
        risk_result = categorizer(
            f"Domain security risk: {summary}",
            candidate_labels=["Low", "Medium", "High"],
            multi_label=False
        )
        risk = risk_result["labels"][0]
        
        return f"""
# Threat Report

**Summary**: {summary}

**Risk Level**: {risk}

**Assessment**: Domain WHOIS data analyzed for potential threats.
"""
        
    except Exception as e:
        return fallback_report(clean_data)

def fallback_report(clean_data):
    """Fallback when models fail"""
    whois_data = clean_data.get('whois', {})
    domain = whois_data.get('domain_name', 'Unknown')
    
    return f"""
# OSINT Threat Report

**Target**: {domain}

**Status**: Data collected successfully

**Summary**: WHOIS information gathered for {domain}. Basic domain registration details available for manual review.

**Risk Level**: Unknown - Manual analysis required

**Next Steps**: 
- Review raw WHOIS data
- Check additional threat intelligence sources
- Verify domain reputation
"""