import unittest
from app.services.strategies.customer_price_strategy import CustomerPriceStrategy
from app.services.strategies.ctv_price_strategy import CtvPriceStrategy
from app.services.strategies.description_strategy import DescriptionStrategy
from app.services.strategies.availability_strategy import AvailabilityStrategy
from app.services.strategies.role_based_strategy import RoleBasedStrategy

class TestStrategies(unittest.TestCase):
    def setUp(self):
        self.query = "haluo"
        self.role = "ctv"

    def test_customer_price_strategy(self):
        result = CustomerPriceStrategy().handle(self.query)
        self.assertIsInstance(result, list)
        self.assertTrue(any("giá khuyến mãi" in r.lower() for r in result))

    def test_ctv_price_strategy(self):
        result = CtvPriceStrategy().handle(self.query)
        self.assertTrue(any("cộng tác viên" in r.lower() for r in result))

    def test_description_strategy(self):
        result = DescriptionStrategy().handle(self.query)
        self.assertTrue(any("mô tả" in r.lower() for r in result))

    def test_availability_strategy(self):
        result = AvailabilityStrategy().handle(self.query)
        self.assertTrue(any("còn hàng" in r.lower() or "hết hàng" in r.lower() for r in result))

    def test_role_based_strategy_ctv(self):
        strategy = RoleBasedStrategy(role=self.role)
        result = strategy.handle(self.query)
        self.assertTrue(any("cộng tác viên" in r.lower() for r in result))

if __name__ == "__main__":
    unittest.main()
