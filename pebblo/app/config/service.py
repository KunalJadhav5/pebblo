from contextlib import redirect_stderr, redirect_stdout
from fastapi import FastAPI
from io import StringIO
import uvicorn
import asyncio

from pebblo.app.routers.local_ui_routers import local_ui_router_instance
from fastapi.staticfiles import StaticFiles
from pathlib import Path

with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
    from pebblo.app.routers.routers import router_instance


class Service:
    def __init__(self, config_details):
        # Initialise app instance
        self.app = FastAPI()
        # Register the router instance with the main app
        self.app.include_router(router_instance.router)
        self.app.include_router(local_ui_router_instance.router)
        # Fetching Details from Config File
        self.config_details = config_details
        self.port = self.config_details.get('daemon', {}).get('port', 8000)
        self.host = self.config_details.get('daemon', {}).get('host', 'localhost')
        self.log_level = self.config_details.get('logging', {}).get('level', 'info')
        self.origins = ['http://localhost:8000',
                        'http://localhost:8080',
                        'http://localhost:8000/pebblo',
                        'http://localhost:8080/pebblo',
                        'http://localhost:8000/pebblo/',
                        'http://localhost:8080/pebblo/'
                        f'http://{self.host}:{self.port}'
                        ]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    async def create_main_api_server(self):
        self.app.mount(
            "/app/pebblo-ui",
            StaticFiles(directory=Path(__file__).parent.parent.absolute() / "pebblo-ui"),
            name="static",
        )
        # Add config Details to Uvicorn
        config = uvicorn.Config(app=self.app, host=self.host, port=self.port, log_level=self.log_level)
        server = uvicorn.Server(config)
        await server.serve()

    def start(self):
        asyncio.run(self.create_main_api_server())



