import abc
import string
import typing

from TreppoApp.types import Command


class CommandDict(typing.TypedDict):
    all: bool
    create: bool
    show: bool
    edit: bool
    delete: bool


class CommandNameDict(typing.TypedDict):
    all: str
    create: str
    show: str
    edit: str
    delete: str


class CommandBuilder(abc.ABC):
    all_endpoint: string.Template | None
    create_endpoint: string.Template | None
    show_endpoint: string.Template | None
    edit_endpoint: string.Template | None
    delete_endpoint: string.Template | None

    _commands: CommandDict
    _context: dict[str, str]
    _also_add: list[Command]

    def __init__(
        self,
        all: str | None,
        create: str | None,
        show: str | None,
        edit: str | None,
        delete: str | None,
        *,
        context: dict[str, str] = {}
    ):
        """Create a new command builder.

        Parameters
        ==========
        all : str | None
            The endpoint for the all route.
        create : str | None
            The endpoint for the create route.
        show : str | None
            The endpoint for the show route.
        edit : str | None
            The endpoint for the edit route.
        delete : str | None
            The endpoint for the delete route.

        context : dict[str, str]
            A dictionary that will be used to replace variables in strings.
            See https://docs.python.org/3/library/string.html#template-strings.
        """
        self.all_endpoint = string.Template(all) if all else None
        self.create_endpoint = string.Template(create) if create else None
        self.show_endpoint = string.Template(show) if show else None
        self.edit_endpoint = string.Template(edit) if edit else None
        self.delete_endpoint = string.Template(delete) if delete else None

        self._commands: CommandDict = {
            "all": False,
            "create": False,
            "show": False,
            "edit": False,
            "delete": False,
        }
        self._names: CommandNameDict = {
            "all": "All",
            "create": "Create",
            "show": "Show",
            "edit": "Edit",
            "delete": "Delete",
        }

        self._context = context
        self._also_add = []

    def set_context(self, context: dict[str, str]) -> typing.Self:
        self._context = context
        return self

    def all(self, name: str) -> typing.Self:
        self._commands["all"] = True
        self._names["all"] = name
        return self

    def create(self, name: str) -> typing.Self:
        self._commands["create"] = True
        self._names["create"] = name
        return self

    def show(self, name: str) -> typing.Self:
        self._commands["show"] = True
        self._names["show"] = name
        return self

    def edit(self, name: str) -> typing.Self:
        self._commands["edit"] = True
        self._names["edit"] = name
        return self

    def delete(self, name: str) -> typing.Self:
        self._commands["delete"] = True
        self._names["delete"] = name
        return self

    def build(self) -> list[Command]:
        cmds: list[Command] = []

        if self._commands["all"] and self.all_endpoint:
            cmds.append(
                Command(
                    self.all_endpoint.safe_substitute(self._context), self._names["all"]
                )
            )
        if self._commands["create"] and self.create_endpoint:
            cmds.append(
                Command(
                    self.create_endpoint.safe_substitute(self._context),
                    self._names["create"],
                )
            )

        if self._commands["show"] and self.show_endpoint:
            cmds.append(
                Command(
                    self.show_endpoint.safe_substitute(self._context),
                    self._names["show"],
                )
            )

        if self._commands["edit"] and self.edit_endpoint:
            cmds.append(
                Command(
                    self.edit_endpoint.safe_substitute(self._context),
                    self._names["edit"],
                )
            )

        if self._commands["delete"] and self.delete_endpoint:
            cmds.append(
                Command(
                    self.delete_endpoint.safe_substitute(self._context),
                    self._names["delete"],
                )
            )

        if self._also_add:
            cmds.extend(self._also_add)

        return cmds

    def also_add(self, commands: list[Command]) -> typing.Self:
        self._also_add.extend(commands)
        return self


class ProjectCommandBuilder(CommandBuilder):
    """
    Substitutes
    ===========
    `id` : The ID of the project
    """

    def __init__(self):
        super().__init__(
            "/",
            "/project/create/",
            "/project/$id/",
            "/project/$id/edit/",
            "/project/$id/delete/",
        )


class CategoryCommandBuilder(CommandBuilder):
    """
    Substitutes
    ===========
    `pid` : The ID of the project associated to the category
    `id` : The ID of the category
    """

    def __init__(self):
        super().__init__(
            None,
            "/project/$pid/category/create/",
            None,
            "/project/$pid/category/$id/edit/",
            "/project/$pid/category/$id/delete/",
        )


class CardCommandBuilder(CommandBuilder):
    """
    Substitutes
    ===========
    `pid` : The ID of the project associated to the category
    `cid` : The ID of the category associated to the card
    `id` : The ID of the card
    """

    def __init__(self):
        super().__init__(
            None,
            "/project/$pid/category/$cid/card/create/",
            "/project/$pid/category/$cid/card/$id/",
            "/project/$pid/category/$cid/card/$id/edit/",
            "/project/$pid/category/$cid/card/$id/delete/",
        )
