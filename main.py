from dotenv import load_dotenv
from app.main.rest.main import prepare_rest_api_server

if __name__ == '__main__':
    load_dotenv()

    app = prepare_rest_api_server()

    import uvicorn
    import os
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
