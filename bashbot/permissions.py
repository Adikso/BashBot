from discord import User

from bashbot import bot


def has_permission(permission_name, user, channel):
    if permission_name is None:
        return True

    if isinstance(user, User):
        user = user.id

    if isinstance(user, str) and user.startswith("<@"):
        user = user[2:-1]

    permission = bot.permissions.get(user)

    if not permission:
        if bot.permissions.get("default"):
            permission = bot.permissions.get("default")
    else:
        if "channels" in permission \
                and channel.id in permission["channels"] \
                and permission_name in permission["channels"][channel.id]:

            permission = permission["channels"][channel.id]

        elif "servers" in bot.permissions.get(user) and hasattr(channel, "server") \
                and channel.server.id in bot.permissions.get(user)["servers"] \
                and permission_name in bot.permissions.get(user)["servers"][channel.server.id]:

            permission = bot.permissions.get(user)["servers"][channel.server.id]

        elif "global" in bot.permissions.get(user) \
                and permission_name in bot.permissions.get(user)["global"]:

            permission = bot.permissions.get(user)["global"]

        elif not user.startswith("&") \
                and has_roles_permission(permission_name, channel.server.get_member(user), channel):

            return True

        elif bot.permissions.get("default"):
            permission = bot.permissions.get("default")

        else:
            return False

    return permission_name in permission and permission[permission_name]


def has_roles_permission(permission_name, user, channel):
    for role in user.roles:
        if has_permission(permission_name, "&" + role.id, channel):
            return True

    return False


def set_permission(permission_name, new_value, user):
    if isinstance(user, User):
        user = user.id

    if isinstance(user, str) and user.startswith("<@"):
        user = user[2:-1]

    permissions = bot.permissions.get(user)

    if not permissions:
        bot.permissions.set(user, {})
        permissions = bot.permissions.get(user)

    parts = permission_name.split(".")

    if parts[0] in ["channels", "servers", "global"]:
        if parts[0] in permissions:
            permissions = permissions[parts[0]]
        else:
            permissions[parts[0]] = {}
            permissions = permissions[parts[0]]

        if parts[0] in ["channels", "servers"]:
            if parts[1].startswith("<#"):
                parts[1] = parts[1][2:-1]

            if parts[1] in permissions:
                permissions = permissions[parts[1]]
            else:
                permissions[parts[1]] = {}
                permissions = permissions[parts[1]]
            permission_name = ".".join(parts[2:])
        else:
            permission_name = ".".join(parts[1:])

    permissions[permission_name] = new_value.lower() == "true"
    bot.permissions.save()
