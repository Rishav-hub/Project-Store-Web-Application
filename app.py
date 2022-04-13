import os
if __name__ == '__main__':
    # os.system('uvicorn project_store_presentation_layer.endpoints:app --reload --host=0.0.0.0 --port=8080')
    os.system('uvicorn project_store_presentation_layer.endpoints:app --reload --host=127.0.0.1 --port=8080')
