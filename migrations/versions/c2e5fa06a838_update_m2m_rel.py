"""Update_m2m_rel

Revision ID: c2e5fa06a838
Revises: 689d7003e74c
Create Date: 2023-07-19 17:21:54.199709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2e5fa06a838'
down_revision = '689d7003e74c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'comments', ['id'])
    op.create_unique_constraint(None, 'estimates', ['id'])
    op.create_unique_constraint(None, 'photos', ['id'])
    op.drop_constraint('tag_photo_association_photo_id_fkey', 'tag_photo_association', type_='foreignkey')
    op.create_foreign_key(None, 'tag_photo_association', 'photos', ['photo_id'], ['id'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'tags', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'tags', type_='unique')
    op.drop_constraint(None, 'tag_photo_association', type_='foreignkey')
    op.create_foreign_key('tag_photo_association_photo_id_fkey', 'tag_photo_association', 'photos', ['photo_id'], ['id'])
    op.drop_constraint(None, 'photos', type_='unique')
    op.drop_constraint(None, 'estimates', type_='unique')
    op.drop_constraint(None, 'comments', type_='unique')
    # ### end Alembic commands ###