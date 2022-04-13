import os
if __name__ == '__main__':
    os.system('uvicorn project_store_presentation_layer.endpoints:app --reload')