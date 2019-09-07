from ..flaskr.model import Location


def test_insert(db_session):
    test_loc_name = 'test_loc'
    new_loc = Location(name=test_loc_name)

    db_session.add(new_loc)
    db_session.commit()

    check_loc = db_session.query(Location).filter_by(name=test_loc_name).first()
    assert check_loc.name == test_loc_name


def test_select(db_session):
    check_loc = db_session.query(Location).filter_by(name='Wadhurst').first()
    assert check_loc is not None


def test_delete(db_session):
    check_loc = db_session.query(Location).filter_by(name='Wadhurst').first()
    if check_loc is not None:
        db_session.delete(check_loc)
        db_session.flush()
        # db_session.commit()
        check_loc = db_session.query(Location).filter_by(name='Wadhurst').first()
        assert check_loc is None
    else:
        assert True is False, 'No row to delete'
