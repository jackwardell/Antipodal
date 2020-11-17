"""deleting old feedback

Revision ID: 896b77348eaf
Revises: bc8e2176b9b4
Create Date: 2020-11-17 23:30:50.152867

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "896b77348eaf"
down_revision = "bc8e2176b9b4"
branch_labels = None
depends_on = None


def upgrade():
    # schema_upgrades()
    data_upgrades()


def downgrade():
    # data_downgrades()
    # schema_downgrades()
    pass


def schema_upgrades():
    """schema upgrade migrations go here."""
    pass


def schema_downgrades():
    """schema downgrade migrations go here."""
    pass


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    from sqlalchemy import orm
    from antipodal.models import Feedback

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.query(Feedback).delete()
    session.commit()


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
