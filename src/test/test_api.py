from pytest import mark
from httpx import AsyncClient


@mark.asyncio
async def test_get_all(async_client: AsyncClient):
    response = await async_client.get("/memes/")

    assert response.status_code == 200


@mark.asyncio
async def test_post(async_client: AsyncClient):
    # with open("test/image.png", "wb") as file:
    #     file.write(b"Hello, world")
    with open("test/image.png", "rb") as file:
        response = await async_client.post(
            "/memes/",
            # files={"data": file, "type": "image/png"},
            files={'file': ("test/image.png", file)}, data={'text': "testing post"}
        )

        assert response.json() == 1
