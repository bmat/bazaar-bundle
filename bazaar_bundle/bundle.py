from pydantic import BaseModel
from dependency_injector import containers, providers
from applauncher.applauncher import Configuration, ServiceContainer
from applauncher.event import KernelShutdownEvent
from bazaar import FileSystem


class BazaarConfig(BaseModel):
    storage_uri: str
    db_uri: str
    default_namespace: str = ""


class BazaarContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=BazaarConfig)
    configuration = Configuration()

    file_system = providers.Singleton(
        FileSystem,
        storage_uri=configuration.provided.bazaar.storage_uri,
        db_uri=configuration.provided.bazaar.db_uri,
        namespace=configuration.provided.bazaar.default_namespace
    )


class BazaarBundle(object):
    def __init__(self):

        self.config_mapping = {
            "bazaar": BazaarConfig
        }

        self.fs = None

        self.event_listeners = [
            (KernelShutdownEvent, self.kernel_shutdown),
        ]

        self.injection_bindings = {
            "bazaar": BazaarContainer
        }

    def kernel_shutdown(self, event):
        ServiceContainer.bazaar.file_system().close()
