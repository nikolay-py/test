"""Test route image_desc_en."""
import requests


def test_health_url(host_name) -> None:
    """Testing /health a positive response expected."""
    api_route = '/health'
    with requests.Session() as s:
        response = s.get(host_name+api_route)
        data = response.json()
    exp_result = 'ok'

    assert response.ok
    assert data == exp_result


def test_image_desc_en(host_name: str, img_path: str) -> None:
    """Testing /api/image_desc_en a positive response expected."""
    api_route = '/api/image_desc_en'
    payload = {'path': img_path}
    with requests.Session() as s:
        response = s.post(host_name+api_route, json=payload)
        data = response.json()
    # exp_result = {
    #     'desc_model_ver': '2021-11-28',
    #     'description': 'a cat is sitting on a chair next to a cat .'
    # }
    assert response.ok
    assert len(data['desc_model_ver']) > 9
    assert len(data['description']) > 5
