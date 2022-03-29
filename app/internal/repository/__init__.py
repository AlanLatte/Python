"""
Module ``Repository`` must contain **CRUD** methods.

Note:
    The repository must contain a minimum set of instructions for interacting with the
    target database.

Examples:
    Let's say we have a User repository. For its correct operation, 5 implemented
    methods are sufficient.::

        class User:
            async def create(self, cmd):
                ...
            async def read(self, query):
                ...
            async def read_all(self):
                ...
            async def update(self, cmd):
                ...
            async def delete(self, cmd):
                ...

    If, for example, you need to update the password, you will need to use 2 methods
    in the implemented service method.::

        class UserService:
            repository: User

            async def change_password(self, cmd: UpdateUserPasswordCommand):
                user = await self.repository.read(cmd=cmd)
                user.password = cmd.password

                return self.repository.update(cmd=cmd)
"""