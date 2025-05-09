import unittest
from app.services.strategies.price_strategy import PriceStrategy
from app.services.strategies.customer_price_strategy import CustomerPriceStrategy
from app.services.strategies.ctv_price_strategy import CtvPriceStrategy
from app.services.strategies.description_strategy import DescriptionStrategy
from app.services.strategies.availability_strategy import AvailabilityStrategy

class TestStrategies(unittest.TestCase):
    def setUp(self):
        self.query = "haluo"

    def test_price_strategy(self):
        result = PriceStrategy().handle(self.query)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_customer_price_strategy(self):
        result = CustomerPriceStrategy().handle(self.query)
        self.assertTrue(all("giá khuyến mãi" in r for r in result))

    def test_ctv_price_strategy(self):
        result = CtvPriceStrategy().handle(self.query)
        self.assertTrue(all("giá dành cho cộng tác viên" in r for r in result))

    def test_description_strategy(self):
        result = DescriptionStrategy().handle(self.query)
        self.assertTrue(all("Mô tả sản phẩm" in r for r in result))

    def test_availability_strategy(self):
        result = AvailabilityStrategy().handle(self.query)
        self.assertTrue(any("còn hàng" in r or "hết hàng" in r for r in result))

if __name__ == "__main__":
    unittest.main()
