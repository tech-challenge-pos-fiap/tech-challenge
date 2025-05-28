from fastapi.testclient import TestClient


def test_create_product(client: TestClient):
    payload = {
        'name': 'Produto Teste',
        'description': 'Descrição de teste',
        'price': 19.99,
        'category': 'burguers'
    }

    response = client.post('/products', json=payload)
    data = response.json()

    assert response.status_code == 201
    assert data['message'] == 'Produto criado com sucesso.'
    assert data['data']['name'] == payload['name']
    assert data['data']['category'] == payload['category']
    assert data['data']['price'] == payload['price']


def test_list_products_by_category(client: TestClient):
    payload = {
        'name': 'Produto Categoria',
        'description': 'Produto para teste de listagem',
        'price': 29.99,
        'category': 'drinks'
    }
    client.post('/products', json=payload)

    response = client.get('/products/category/drinks')
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert any(prod['category'] == 'drinks' for prod in data)


def test_update_product(client: TestClient):
    payload = {
        'name': 'Produto para Update',
        'description': 'Descrição inicial',
        'price': 10.0,
        'category': 'appetizers'
    }
    response_create = client.post('/products', json=payload)
    product_id = response_create.json()['data'].get('id')  # precisa retornar id

    updated_payload = {
        'name': 'Produto Atualizado',
        'description': 'Descrição atualizada',
        'price': 15.0,
        'category': 'burguers'
    }

    response_update = client.put(f'/products/{product_id}', json=updated_payload)
    data = response_update.json()

    assert response_update.status_code == 200
    assert data['message'] == 'Produto atualizado com sucesso.'
    assert data['data']['name'] == 'Produto Atualizado'
    assert data['data']['category'] == 'burguers'


def test_delete_product(client: TestClient):
    payload = {
        'name': 'Produto para Deletar',
        'description': 'Será deletado',
        'price': 5.0,
        'category': 'desserts'
    }
    response_create = client.post('/products', json=payload)
    product_id = response_create.json()['data'].get('id')

    response_delete = client.delete(f'/products/{product_id}')
    data = response_delete.json()

    assert response_delete.status_code == 200
    assert data['message'] == 'Produto deletado com sucesso.'

    response_delete_again = client.delete(f'/products/{product_id}')
    assert response_delete_again.status_code == 404
