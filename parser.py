from liblet import Tree, AnnotatedTreeWalker
from grammar import Logo

logoast = AnnotatedTreeWalker("name")
brackets = ["(", ")", "[", "]", "-", "+"]


@logoast.register
def prog(visit, parse_tree):
    return Tree(
        {"type": parse_tree.root["name"]},
        [
            visit(child)
            for child in parse_tree.children
            if child.root["name"] != "EOL" and len(child.children) > 0
        ],
    )


@logoast.register
def line(visit, parse_tree):
    return Tree({"type": "line"}, [visit(child) for child in parse_tree.children])


@logoast.register
def cmd(visit, parse_tree):
    if parse_tree.children[0].children[0].root["name"] in brackets:
        if parse_tree.children[0].root["name"] == "procedureInvocation":
            return Tree(
                {
                    "type": "procedureInvocation",
                    "name": parse_tree.children[0]
                    .children[1]
                    .children[0]
                    .root["value"],
                },
                [
                    visit(child)
                    for child in parse_tree.children[0].children[2:]
                    if child.root["name"] != "EOL"
                    and child.root["name"] not in brackets
                    and child.root["type"] != "token"
                ],
            )
        else:
            return Tree(
                {"type": "command", "name": parse_tree.children[0].root["name"]},
                [
                    visit(child)
                    for child in parse_tree.children[0].children
                    if child.root["type"] != "token"
                ],
            )
    else:
        if parse_tree.children[0].root["name"] == "procedureInvocation":
            return Tree(
                {
                    "type": "procedureInvocation",
                    "name": parse_tree.children[0]
                    .children[0]
                    .children[0]
                    .root["value"],
                },
                [
                    visit(child)
                    for child in parse_tree.children[0].children[1:]
                    if child.root["name"] != "EOL"
                ],
            )
        else:
            return Tree(
                {"type": "command", "name": parse_tree.children[0].root["name"]},
                [
                    visit(child)
                    for child in parse_tree.children[0].children[1:]
                    if child.root["name"] != "EOL"
                ],
            )


@logoast.register
def procedureInvocation(visit, parse_tree):
    if parse_tree.children[0].root["name"] in brackets:
        return Tree(
            {
                "type": "procedureInvocation",
                "name": parse_tree.children[1].children[0].root["value"],
            },
            [visit(child) for child in parse_tree.children[2:-1]],
        )
    else:
        return Tree(
            {
                "type": "procedureInvocation",
                "name": parse_tree.children[0].children[0].root["value"],
            },
            [visit(child) for child in parse_tree.children[1:]],
        )


@logoast.register
def procedureDeclaration(visit, parse_tree):
    p = [
        child.children[1].children[0].root["value"]
        for child in parse_tree.children
        if child.root["name"] == "parameterDeclarations"
    ]
    return Tree(
        {
            "type": "procedureDeclaration",
            "name": parse_tree.children[1].children[0].root["value"],
            "params": p,
        },
        [
            visit(child)
            for child in parse_tree.children[2:-1]
            if (child.root["name"] == "line" or child.root["name"] == "retCmd")
            and child.root["name"] != "parameterDeclarations"
        ],
    )


@logoast.register
def expression(visit, parse_tree):
    sign = [
        child.root["name"]
        for child in parse_tree.children
        if child.root["name"] == "+" or child.root["name"] == "-"
    ]
    count = 0
    if len(sign) > 0:
        for n in sign:
            if n == "-":
                count += 1
        if count % 2 == 0:
            return Tree(
                {"type": "expression", "sign": "+"},
                [
                    visit(child)
                    for child in parse_tree.children
                    if child.root["name"] not in brackets
                    and child.root["name"] != "EOL"
                ],
            )
        else:
            return Tree(
                {"type": "expression", "sign": "-"},
                [
                    visit(child)
                    for child in parse_tree.children
                    if child.root["name"] not in brackets
                    and child.root["name"] != "EOL"
                ],
            )
    return Tree(
        {"type": "expression"},
        [
            visit(child)
            for child in parse_tree.children
            if child.root["name"] not in brackets and child.root["name"] != "EOL"
        ],
    )


@logoast.register
def addsuboperators(visit, parse_tree):
    return Tree({"type": "addsubOperator", "name": parse_tree.children[0].root["name"]})


@logoast.register
def muldivoperators(visit, parse_tree):
    return Tree(
        {"type": "muldivOperator", "name": parse_tree.children[0].root["value"]}
    )


@logoast.register
def number(visit, parse_tree):
    return Tree({"type": "valueNumber", "value": parse_tree.children[0].root["value"]})


@logoast.register
def BOOLEAN(visit, parse_tree):
    return Tree({"type": "boolean", "value": parse_tree.root["value"]})


@logoast.register
def block(visit, parse_tree):
    return Tree(
        {"type": "block"},
        [
            visit(child)
            for child in parse_tree.children[1:-1]
            if child.root["name"] != "EOL"
        ],
    )


@logoast.register
def compareOperator(visit, parse_tree):
    return Tree(
        {"type": "compareOperator", "value": parse_tree.children[0].root["value"]}
    )


@logoast.register
def parameters(visit, parse_tree):
    return Tree({"type": "parameter"}, [visit(child) for child in parse_tree.children])


@logoast.register
def deref(visit, parse_tree):
    if parse_tree.children[0].root["name"] == ":":
        return Tree(
            {"type": "deref", "name": parse_tree.children[1].children[0].root["value"]}
        )
    elif parse_tree.children[1].root["name"] == "name":
        return Tree(
            {"type": "deref", "name": parse_tree.children[1].children[0].root["value"]}
        )
    elif parse_tree.children[1].root["name"] == "deref":
        return Tree(
            {"type": "deref"}, [visit(child) for child in parse_tree.children[1:]]
        )
    else:
        name = parse_tree.children[1].root["value"]
        return Tree({"type": "deref", "name": name[1:]})


@logoast.register
def STRINGLITERAL(visit, parse_tree):
    name = parse_tree.root["value"]
    return Tree({"type": "string", "name": name[1:]})


@logoast.register
def parameterDeclarations(visit, parse_tree):
    return Tree(
        {
            "type": "parameterDeclaration",
            "name": parse_tree.children[1].children[0].root["value"],
        }
    )


@logoast.register
def stat(visit, parse_tree):
    return Tree(
        {"type": parse_tree.children[0].root["name"]},
        [visit(child) for child in parse_tree.children[0].children[1:]],
    )


@logoast.register
def retCmd(visit, parse_tree):
    if parse_tree.children[0].root["name"] == "stop":
        return Tree({"type": "command", "name": "stop"})
    else:
        return Tree(
            {"type": "command", "name": "output"},
            [visit(child) for child in parse_tree.children[0].children[1:]],
        )


@logoast.register
def colorBlock(visit, parse_tree):
    return Tree(
        {"type": "rgbList"},
        [
            visit(child)
            for child in parse_tree.children[1:-1]
            if child.root["name"] != "EOL"
        ],
    )


def parse(source):
    try:
        return logoast(Logo.tree(source, "prog"))
    except Exception:
        print("PARSING ERROR")
