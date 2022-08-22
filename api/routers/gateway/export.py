from .messages.clientbound.register import clientbound_messages
from .messages.serverbound.register import serverbound_messages

TYPES = {"integer": "number"}
IMPORTS = {"Page": "@/stores/page"}


def totype(name: str, prop: dict[str, str], required: set[str], imports: dict[str, set[str]]) -> str:
    if "$ref" in prop:
        typename = prop["$ref"].split("/")[-1]

        if typename not in imports:
            source = IMPORTS[typename]
            if source not in imports:
                imports[source] = set()

            imports[source].add(typename)
    else:
        typename = TYPES.get(prop["type"], prop["type"])

    req = "" if name in required else "?"
    return f"{name}{req}: {typename}"


def tointerface(schema: dict, sep: str = ", ", imports: dict[str, set[str]] = {}) -> str:
    required = set(schema.get("required", []))
    props = sep.join(totype(name, prop, required, imports) for name, prop in schema["properties"].items())
    return "{" + props + "}"


def export_messages():
    messages: list[tuple[str, str]] = []
    for msgid, cls in serverbound_messages.items():
        interface = tointerface(cls.schema())
        message = f"type {cls.__name__} = IServerBound<{msgid!r}, {interface}>;"
        messages.append((cls.__name__, message))

    with open("/app/serverbound.ts", "w") as f:
        types = " | ".join(msgid for msgid, _ in messages)
        f.write("\n".join(msg for _, msg in messages))
        f.write("\n\n")
        f.write(f"export type ServerBound = {types};\n")

    messages: list[tuple[str, str, str]] = []
    imports: dict[str, set[str]] = {}
    for msgid, cls in clientbound_messages.items():
        interface = tointerface(cls.schema(), "; ", imports)
        message = f"interface {cls.__name__} {interface};"
        messages.append((msgid, cls.__name__, message))


    def toset(names: set) -> str:
        return "{ " + ", ".join(sorted(names)) + " }"

    with open("/app/clientbound.ts", "w") as f:
        types = "{\n" + "".join(f"\t{msgid}: {clsname};\n" for msgid, clsname, _ in messages) + "}"

        f.write("\n".join(f"import {toset(names)} from {source!r}" for source, names in imports.items()))
        f.write("\n\n")
        f.write("\n\n".join(msg for _, _, msg in messages))
        f.write("\n\n")
        f.write(f"export type ClientBoundMessages = {types};\n")

    with open("/app/clientbound.ts", "r") as f:
        print(f.read())
