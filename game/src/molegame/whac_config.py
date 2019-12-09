from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class WhacConfig:
    kubernetes_config: Optional[str]
    deployment_image_mole: str
    deployment_image_relay: str
    deployment_name: str
    namespace: str
    minikube_ip: str
    containers_port: int
    host_port: int

    @property
    def deployment_name_mole(self) -> str:
        return self.deployment_name + '-mole-prod'

    @property
    def deployment_name_relay(self) -> str:
        return self.deployment_name + '-relay-prod'

    @property
    def deployment_names(self) -> List[str]:
        return [self.deployment_name_mole, self.deployment_name_relay]
