def clean(raw_data):
    cleaned = {}
    for key,data in raw_data.items():
        if isinstance(data, dict) and "error" in data:
            continue
        cleaned[key] = str(data)
    return cleaned
