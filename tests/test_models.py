
def test_create_product():
    product = Product(name='Тест', quantity=10, price=100)
    assert product.name == 'Тест'
    assert product.quantity == 10