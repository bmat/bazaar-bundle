from typing import Dict, List, Optional

from applauncher.applauncher import Configuration, ServiceContainer
from applauncher.event import KernelShutdownEvent
from bazaar import FileSystem
from dependency_injector import containers, providers
from pydantic import BaseModel


class FileSystemConfig(BaseModel):
    storage_uri: str
    db_uri: str
    default_namespace: str = ""


class NamedFileSystemConfig(BaseModel):
    name: str
    storage_uri: str
    db_uri: str
    default_namespace: str = ""


class BazaarConfig(FileSystemConfig):
    file_systems: Optional[List[NamedFileSystemConfig]]


class FileSystemCollection:
    def __init__(self, file_systems: List[Dict[str, str]]):
        self._file_systems = {
            fs.name: FileSystem(storage_uri=fs.storage_uri, db_uri=fs.db_uri, namespace=fs.default_namespace)
            for fs in file_systems or []
        }

    def __getitem__(self, fs_name: str) -> FileSystem:
        """Allow subscribe getting: FileSystemCollection()['default']"""
        return self._file_systems[fs_name]

    def __getattr__(self, fs_name: str) -> FileSystem:
        """Allow dot getting: FileSystemCollection().default"""
        return self._file_systems[fs_name]

    def get(self, fs_name: str) -> Optional[FileSystem]:
        """
        Fetch the provided name or None if non existent.
        The other two methods will fail if name doesn't exist.
        """
        return self._file_systems.get(fs_name)


class BazaarContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=BazaarConfig)
    configuration = Configuration()

    file_system = providers.Singleton(
        FileSystem,
        storage_uri=configuration.provided.bazaar.storage_uri,
        db_uri=configuration.provided.bazaar.db_uri,
        namespace=configuration.provided.bazaar.default_namespace
    )

    file_systems = providers.Singleton(
        FileSystemCollection,
        file_systems=configuration.provided.bazaar.file_systems
    )


class BazaarBundle(object):
    def __init__(self):

        self.config_mapping = {
            "bazaar": BazaarConfig
        }

        # TODO: What is this used for?
        self.fs = None

        self.event_listeners = [
            (KernelShutdownEvent, self.kernel_shutdown),
        ]

        self.injection_bindings = {
            "bazaar": BazaarContainer
        }

    def kernel_shutdown(self, event):
        ServiceContainer.bazaar.file_system().close()
