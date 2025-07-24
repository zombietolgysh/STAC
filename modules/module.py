class STCModule:
    def __init__(self):
        print(f"[SYSTEM] Initializing: {self.__class__.__name__}")
    
    def ready(self):
        print(f"[INFO]{self.__class__.__name__} is ready")

    def process(self):
        pass

    def stop(self):
        print(f"[SYSTEM] Stopping: {self.__class__.__name__}"