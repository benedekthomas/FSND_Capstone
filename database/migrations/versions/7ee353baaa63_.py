"""empty message

Revision ID: 7ee353baaa63
Revises: 
Create Date: 2020-09-12 16:52:19.492870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ee353baaa63'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('position', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('kudos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=200), nullable=True),
    sa.Column('team_member_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['team_member_id'], ['team_members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('kudos')
    op.drop_table('team_members')
    # ### end Alembic commands ###