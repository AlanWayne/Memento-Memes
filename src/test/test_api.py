from httpx import AsyncClient


async def test_post(async_client: AsyncClient):
    with open("test/image.png", "rb") as file:
        response = await async_client.post(
            "/memes/",
            files={'file': ("test/image.png", file)}, data={'text': "testing post"}
        )

    assert response.status_code == 200
    assert response.json()['id'] is not None
    assert response.json()['path'].startswith('app/media/')
    assert response.json()['text'] == 'testing post'


async def test_put(async_client: AsyncClient):
    sub_response = await async_client.get("/memes/")
    put_id = sub_response.json()[-1]['id']

    response = await async_client.put(
        f"/memes/{put_id}",
        data={'text': 'testing put'},
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json()['id'] == put_id
    assert response.json()['path'].startswith('app/media/')
    assert response.json()['text'] == 'testing put'


async def test_get_all(async_client: AsyncClient):
    response = await async_client.get("/memes/")

    assert response.status_code == 200


async def test_get(async_client: AsyncClient):
    sub_response = await async_client.get("/memes/")
    get_id = sub_response.json()[-1]['id']

    response = await async_client.get(f"/memes/{get_id}")

    assert response.status_code == 200
    assert response.json()['path'].startswith('app/media/')
    assert response.json()['text'] == 'testing put'


async def test_del(async_client: AsyncClient):
    sub_response = await async_client.get("/memes/")
    del_id = sub_response.json()[-1]['id']

    response = await async_client.delete(f"/memes/{del_id}")

    assert response.status_code == 200

    response = await async_client.get(f"/memes/{del_id}")

    assert response.json()['status_code'] == 500
