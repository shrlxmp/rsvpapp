import os
import sys

import click
from mongoengine.queryset.visitor import Q

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rsvp.models import User


@click.group()
def cli():
    """A CLI to manage users"""


@click.command()
@click.option('--roles', type=str)
@click.option('--users', type=str, default='')
@click.option('--all', default=False, is_flag=True)
def add_role(roles, users, all):
    """Add specified roles for a user."""
    click.echo('Adding role')
    print(roles)
    roles = roles.split(',')
    for role in roles:
        if all:
            User.objects(roles__nin=[role]).update(push__roles=roles)
        else:
            for user in users.split(','):
                print(user)
                User.objects(Q(email=user) & Q(roles__nin=[role])).update(
                    push__roles=roles
                )


cli.add_command(add_role)
if __name__ == '__main__':
    cli()
