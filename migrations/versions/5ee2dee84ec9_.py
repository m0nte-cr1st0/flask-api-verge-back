"""empty message

Revision ID: 5ee2dee84ec9
Revises: 
Create Date: 2019-10-10 18:30:16.948880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ee2dee84ec9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('versions',
    sa.Column('id', sa.Float(), nullable=False),
    sa.Column('file', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('versions')
    op.drop_table('applications')
    # ### end Alembic commands ###
