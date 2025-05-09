# app/services/strategies/role_based_strategy.py

from services.strategies.customer_price_strategy import CustomerPriceStrategy
from services.strategies.ctv_price_strategy import CtvPriceStrategy
from services.strategies.base_strategy import BaseStrategy

class RoleBasedStrategy(BaseStrategy):
    def __init__(self, role):
        if role == "ctv":
            self.strategy = CtvPriceStrategy()
        else:
            self.strategy = CustomerPriceStrategy()

    def handle(self, user_input):
        return self.strategy.handle(user_input)
