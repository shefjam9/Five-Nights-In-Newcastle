def log(string, type="DEBUG"):
    allowed_types = ["DEBUG", "INFO", "WARNING", "ERROR"]
    if type.upper() in allowed_types:
        print(f"{type.upper()} \t> {string}")
    else:
        print(f"OTHER \t> {string}")