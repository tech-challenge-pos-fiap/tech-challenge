from abc import ABC, abstractmethod
from typing import Dict, Any


class OrderPort(ABC):
    @abstractmethod
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um pedido"""
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancela um pedido"""
        pass

    @abstractmethod
    def update_order(self, order_id: str, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um pedido"""
        pass

    @abstractmethod
    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Obtém um pedido"""
        pass

    @abstractmethod
    def get_orders(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém uma lista de pedidos com base em filtros"""
        pass
