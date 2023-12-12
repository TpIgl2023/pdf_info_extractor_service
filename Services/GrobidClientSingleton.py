from grobid_client.grobid_client import GrobidClient

class GrobidClientSingleton:
    _instance = None

    def __new__(cls, config_path="./grobid_client_python/config.json"):
        if not cls._instance:
            cls._instance = super(GrobidClientSingleton, cls).__new__(cls)
            # Initialize the GrobidClient object here with the provided config_path
            cls._instance.grobid_client = GrobidClient(config_path=config_path)
        return cls._instance