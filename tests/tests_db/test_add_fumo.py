from app.db.requests import db_add_fumo, db_get_fumo_by_name
from app.db.models import Fumo


async def test_db_add_fumo(async_session):
    name = "test"
    file_id = "test"
    source_link = "test"
    await db_add_fumo(async_session, name, file_id, source_link)
    fumo = await db_get_fumo_by_name(async_session, fumo_name=name)
    assert isinstance(fumo, Fumo)
    assert fumo.name == name
    assert fumo.file_id == file_id
    assert fumo.source_link == source_link
