#!/usr/bin/env python3

#####################################################################
# This script demonstrates the duck typing behavior of ViZDoom Enums.
# Check documentation: https://vizdoom.farama.org/api/python/enums/
#####################################################################

from enum import Enum, IntEnum

import vizdoom as vzd


def is_enum_like(obj: object) -> bool:
    """Checks whether a ViZDoom object is Enum"""
    return (
        hasattr(type(obj), "__members__")
        and hasattr(obj, "__int__")
        and hasattr(obj, "__index__")
        and hasattr(obj, "value")
        and isinstance(getattr(obj, "value"), int)
    )


print("Example: vzd.Mode.PLAYER")
print("=== Type Info ===")
print("Type:\t\t\t", type(vzd.Mode.PLAYER))
print("Base classes:\t\t", type(vzd.Mode.PLAYER).__bases__)
print("Is instance of int?\t", isinstance(vzd.Mode.PLAYER, int))
print("Is instance of Enum?\t", isinstance(vzd.Mode.PLAYER, Enum))
print("Is instance of IntEnum?\t", isinstance(vzd.Mode.PLAYER, IntEnum))
print("Is subclass of IntEnum?\t", issubclass(type(vzd.Mode.PLAYER), IntEnum))
print("Is instance of object?\t", isinstance(vzd.Mode.PLAYER, object))
print("Is enum-like?\t\t", is_enum_like(vzd.Mode.PLAYER))

print("\n=== Behavior ====")
print("int(vzd.Mode.PLAYER):\t", int(vzd.Mode.PLAYER))
print("vzd.Mode.PLAYER.value:\t", vzd.Mode.PLAYER.value)
print(
    "vzd.Mode.PLAYER as index:[3, 2, 1][vzd.Mode.PLAYER] =", [3, 2, 1][vzd.Mode.PLAYER]
)
print(
    "vzd.Mode.__members__: \t",
    getattr(vzd.Mode, "__members__", "No __members__ attribute"),
)
