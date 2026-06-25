from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ChainGuard:
    """
    Chain Guard v1.0.
    Защита от каскадных ошибок и семантического дрейфа между агентами.
    """
    def __init__(self):
        self.invariants = {} # Замороженные данные

    def lock_invariants(self, data: Dict[str, Any]) -> None:
        """Фиксация эталонных параметров на старте цепочки."""
        self.invariants = data.copy()
        print(f"🔒 [CHAIN_GUARD] Invariants Locked: {list(self.invariants.keys())}")

    def verify_transfer(self, agent_data: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
        """Сверка данных при передаче между агентами."""
        
        # 1. Проверка на изменение замороженных данных (например, базовой цены)
        for key, expected_val in self.invariants.items():
            if key in agent_data:
                actual_val = agent_data[key]
                if actual_val != expected_val:
                    return {
                        "status": "VIOLATION",
                        "reason": f"Invariant breach: {key} changed from {expected_val} to {actual_val}",
                        "agent": agent_id
                    }

        # 2. Математическая проверка (final_price = base - discount)
        if all(k in agent_data for k in ["base_price", "discount", "final_price"]):
            calculated = agent_data["base_price"] - agent_data["discount"]
            if abs(agent_data["final_price"] - calculated) > 0.01:
                return {
                    "status": "VIOLATION",
                    "reason": f"Logic Desync: Final price {agent_data['final_price']} != {calculated}",
                    "agent": agent_id
                }

        return {"status": "SYNCED"}