from tickets.app import db
from tickets.models import Event


def main():
    with db.db_engine.atomic():
        Event.create(price=2500, title='METZ', description='at Logo')


if __name__ == '__main__':
    main()
