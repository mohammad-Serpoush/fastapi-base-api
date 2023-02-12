"""initial

Revision ID: d50cd45791bd
Revises:
Create Date: 2023-02-12 13:34:20.372684

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd50cd45791bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('persian_name', sa.String(length=100), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('first_name', sa.String(length=255), nullable=True),
                    sa.Column('last_name', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=100), nullable=False),
                    sa.Column('phone_number', sa.String(length=13), nullable=True),
                    sa.Column('hashed_password', sa.String(length=255), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('role_id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('phone_number')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
