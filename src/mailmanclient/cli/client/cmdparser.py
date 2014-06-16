# Copyright (C) 2010-2014 by the Free Software Foundation, Inc.
#
# This file is part of mailman.client.
#
# mailman.client is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailman.client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailman.client.  If not, see <http://www.gnu.org/licenses/>.

from argparse import ArgumentParser
from core.lists import Lists
from core.users import Users
from lib.utils import Colorizer
from core.domains import Domains
from mailmanclient import Client
from mailmanclient._client import MailmanConnectionError


class CmdParser():
    def __init__(self, command):
        parser = ArgumentParser(description='Mailman Command Tools')
        self.initialize_options(parser)
        self.arguments = vars(parser.parse_args())

    def initialize_options(self, parser):
        action = parser.add_subparsers(dest='action')

        # Parser for the action `show`
        action_show = action.add_parser('show')
        scope = action_show.add_subparsers(dest='scope')

        # Show lists
        show_list = scope.add_parser('list')
        show_list.add_argument('list',
                               help='List details about LIST',
                               nargs='?')
        show_list.add_argument('-d',
                               '--domain',
                               help='Filter by DOMAIN')
        show_list.add_argument('-v',
                               '--verbose',
                               help='Detailed listing',
                               action='store_true')
        show_list.add_argument('--no-header',
                               help='Omit headings in detailed listing',
                               action='store_true')

        # Show domains
        show_domain = scope.add_parser('domain')
        show_domain.add_argument('domain',
                                 help='List details about DOMAIN',
                                 nargs='?')
        show_domain.add_argument('-v',
                                 '--verbose',
                                 help='Detailed listing',
                                 action='store_true')
        show_domain.add_argument('--no-header',
                                 help='Omit headings in detailed listing',
                                 action='store_true')

        # Show users
        show_user = scope.add_parser('user')
        show_user.add_argument('user',
                               help='List details about USER',
                               nargs='?')
        show_user.add_argument('-v',
                               '--verbose',
                               help='Detailed listing',
                               action='store_true')
        show_user.add_argument('--no-header',
                               help='Omit headings in detailed listing',
                               action='store_true')
        show_user.add_argument('-l',
                               '--list',
                               help='Specify list name',
                               dest='list_name')

        # Parser for the action `create`
        action_create = action.add_parser('create')
        scope = action_create.add_subparsers(dest='scope')

        # Create list
        create_list = scope.add_parser('list')
        create_list.add_argument('list',
                                 help='List name. e.g., list@domain.org')
        # Create domain
        create_domain = scope.add_parser('domain')
        create_domain.add_argument('domain',
                                   help='Create domain DOMAIN')
        create_domain.add_argument('--contact',
                                   help='Contact address for domain')
        # Create users
        create_user = scope.add_parser('user')
        create_user.add_argument('email',
                                 help='Create user foo@bar.com')
        create_user.add_argument('--password',
                                 help='User password',
                                 required=True)
        create_user.add_argument('--name',
                                 help='Display name of the user',
                                 required=True)

        # Parser for the action `delete`
        action_delete = action.add_parser('delete')
        scope = action_delete.add_subparsers(dest='scope')

        # Delete list
        delete_list = scope.add_parser('list')
        delete_list.add_argument('list',
                                 help='List name. e.g., list@domain.org')
        delete_list.add_argument('--yes',
                                 help='Force delete',
                                 action='store_true')
        # Delete domain
        delete_domain = scope.add_parser('domain')
        delete_domain.add_argument('domain',
                                   help='Domain name. e.g., domain.org')
        delete_domain.add_argument('--yes',
                                   help='Force delete',
                                   action='store_true')
        # Delete user
        delete_user = scope.add_parser('user')
        delete_user.add_argument('user',
                                 help='User email e.g., foo@bar.com')
        delete_user.add_argument('--yes',
                                 help='Force delete',
                                 action='store_true')

        # Parser for the action `subscribe`
        action_subscribe = action.add_parser('subscribe')
        scope = action_subscribe.add_subparsers(dest='scope')
        subscribe_user = scope.add_parser('user')
        subscribe_user.add_argument('users',
                                    help='User email list',
                                    nargs='+')
        subscribe_user.add_argument('-l',
                                    '--list',
                                    help='Specify list name',
                                    dest='list_name',
                                    required=True)
        subscribe_user.add_argument('--quiet',
                                    help='Do not display feedback',
                                    action='store_true')

        # Parser for the action `unsubscribe`
        action_subscribe = action.add_parser('unsubscribe')
        scope = action_subscribe.add_subparsers(dest='scope')
        subscribe_user = scope.add_parser('user')
        subscribe_user.add_argument('users',
                                    help='User email list',
                                    nargs='+')
        subscribe_user.add_argument('-l',
                                    '--list',
                                    help='Specify list name',
                                    dest='list_name',
                                    required=True)
        subscribe_user.add_argument('--quiet',
                                    help='Do not display feedback',
                                    action='store_true')
        # Global options
        parser.add_argument('--host', help='REST API host address',
                            default='http://127.0.0.1')
        parser.add_argument('--port', help='REST API host port',
                            default='8001')
        parser.add_argument('--restuser', help='REST API username',
                            default='restadmin')
        parser.add_argument('--restpass', help='REST API password',
                            default='restpass')

    def manage_list(self, client):
        try:
            lists = Lists(client)
        except MailmanConnectionError:
            raise Exception('Connection to REST API failed')
        action_name = self.arguments['action']
        action = getattr(lists, action_name)
        action(self.arguments)

    def manage_domain(self, client):
        try:
            domains = Domains(client)
        except MailmanConnectionError:
            raise Exception('Connection to REST API failed')
        action_name = self.arguments['action']
        action = getattr(domains, action_name)
        action(self.arguments)

    def manage_user(self, client):
        try:
            users = Users(client)
        except MailmanConnectionError:
            raise Exception('Connection to REST API failed')
        action_name = self.arguments['action']
        action = getattr(users, action_name)
        action(self.arguments)

    def run(self):
        method_name = 'manage_' + self.arguments['scope']
        host = self.arguments['host']
        port = self.arguments['port']
        username = self.arguments['restuser']
        password = self.arguments['restpass']
        client = Client('%s:%s/3.0' % (host, port),
                        username,
                        password)
        method = getattr(self, method_name)
        try:
            method(client)
        except Exception as e:
            colorize = Colorizer()
            colorize.error(e)
            exit(1)
