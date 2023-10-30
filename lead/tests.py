# import pytest
# from django.urls import reverse
# from django.test import Client
#
#
# @pytest.fixture
# def client():
#     return Client()
#
#
# @pytest.mark.django_db
# def test_lead_create_endpoint(client):
#     url = reverse('leadsource1', kwargs={'user_id': '64808b27-febc-4911-a858-4c971462e5e6'})
#     response = client.post(url, data={'leadsource': 'Some lead source'})
#     print("response", response)
#     assert response.status_code == 201
#     assert response.data['leadsource'] == 'Some lead source'


# test.py
import pytest

# app.py
def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def multiply_numbers(a, b):
    return a * b

def divide_numbers(a, b):
    return a / b


def test_addition():
    result = add_numbers(2, 2)
    assert result == 4

def test_subtraction():
    result = subtract_numbers(5, 3)
    assert result == 2

def test_multiplication():
    result = multiply_numbers(2, 3)
    assert result == 6

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        result = divide_numbers(4, 0)
