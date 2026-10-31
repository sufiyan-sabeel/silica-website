"""Every Silica program shown on the website, in one place.

`tools/verify_snippets.py` runs each of these through the real Silica
implementation in the repository, so the site cannot drift from the language.
Nothing here is illustrative pseudocode: each entry is a complete program.
"""

SNIPPETS = {
    # ---------------------------------------------------------------- basics
    "hello": {
        "file": "hello.sc",
        "code": """sfn main() {
    sprint("Hello from Silica")
}""",
    },
    "hero": {
        "file": "hello.sc",
        "code": """sfn main() {
    let name: String = "Silica"
    let year: Int = 2026
    sprint("Hello from " + name)
    sprint("Built in " + str(year))
}""",
    },
    "variables": {
        "file": "variables.sc",
        "code": """sfn noop() {
}

sfn main() {
    let count: Int = 3
    let ratio: Float = 0.75
    let label: String = "silica"
    let ready: Bool = oui
    let nothing: Unit = noop()
    const version: String = "0.9.0"

    sprint(type_of(count))
    sprint(type_of(ratio))
    sprint(type_of(label))
    sprint(type_of(ready))
    sprint(type_of(nothing))
    sprint(version)
}""",
    },
    "types_table": {
        "file": "types.sc",
        "code": """sfn main() {
    let total: Int = 42
    let pi: Float = 3.14159
    let name: String = "Silica"
    let ok: Bool = oui
    let items: List = [1, 2, 3]
    let record: Map = {"language": "Silica", "version": "0.9.0"}

    sprint(total + 1)
    sprint(pi * 2.0)
    sprint(name[0])
    sprint(non ok)
    sprint(len(items))
    sprint(record["version"])
}""",
    },
    # ------------------------------------------------------------- functions
    "functions": {
        "file": "functions.sc",
        "code": """sfn greet(name: String) -> String {
    ret "Hello, " + name
}

sfn add(a: Int, b: Int) -> Int {
    ret a + b
}

sfn main() {
    sprint(greet("Silica"))
    sprint(add(19, 23))
}""",
    },
    "recursion": {
        "file": "fibonacci.sc",
        "code": """sfn fib(n: Int) -> Int {
    si n < 2 {
        ret n
    }
    ret fib(n - 1) + fib(n - 2)
}

sfn main() {
    per i in range(0, 11) {
        dit(fib(i))
        dit(" ")
    }
    sprint("")
}""",
    },
    "unit_function": {
        "file": "unit.sc",
        "code": """sfn banner(title: String) {
    sprint("== " + title + " ==")
}

sfn main() {
    banner("Silica")
}""",
    },
    # ------------------------------------------------------------ conditions
    "conditions": {
        "file": "conditionals.sc",
        "code": """sfn main() {
    let score: Int = 85
    si score >= 50 {
        sprint("Pass")
    } sino {
        sprint("Fail")
    }
}""",
    },
    "logic": {
        "file": "logic.sc",
        "code": """sfn main() {
    let ready: Bool = oui
    let blocked: Bool = nein

    si ready und non blocked {
        sprint("Ready")
    } sino {
        sprint("Not ready")
    }

    si ready ou blocked {
        sprint("At least one is true")
    }
}""",
    },
    "nested_if": {
        "file": "grades.sc",
        "code": """sfn grade(score: Int) -> String {
    si score >= 90 {
        ret "A"
    } sino {
        si score >= 75 {
            ret "B"
        } sino {
            ret "C"
        }
    }
}

sfn main() {
    sprint(grade(94))
    sprint(grade(80))
    sprint(grade(61))
}""",
    },
    # ----------------------------------------------------------------- loops
    "loops": {
        "file": "loops.sc",
        "code": """sfn main() {
    let total: Int = 0
    per i in range(1, 11) {
        total = total + i
    }
    sprint(total)

    let n: Int = 5
    tant n > 0 {
        dit(n)
        dit(" ")
        n = n - 1
    }
    sprint("")
}""",
    },
    "loop_control": {
        "file": "loop_control.sc",
        "code": """sfn main() {
    per i in range(1, 11) {
        si i == 4 {
            continue
        }
        si i == 7 {
            break
        }
        dit(i)
        dit(" ")
    }
    sprint("")
}""",
    },
    "loop_over_list": {
        "file": "loop_list.sc",
        "code": """sfn main() {
    let languages: List = ["Silica", "Python", "Rust"]
    per name in languages {
        sprint(name)
    }
}""",
    },
    # --------------------------------------------------------------- strings
    "strings": {
        "file": "strings.sc",
        "code": """use string

sfn main() {
    let line: String = "silica,language,bytecode"
    let parts: List = string.split(line, ",")

    per part in parts {
        sprint(string.upper(part))
    }

    sprint(string.join(parts, " | "))
    sprint(string.replace(line, ",", " "))
    sprint(string.starts_with(line, "silica"))
    sprint(len(line))
    sprint(line[0])
}""",
    },
    "string_delimiters": {
        "file": "delimiters.sc",
        "code": """sfn main() {
    let single: String = 'single quotes'
    let double: String = "double quotes"
    let block: String = \"\"\"triple quotes
can span lines\"\"\"

    sprint(single)
    sprint(double)
    sprint(block)
    sprint("escape: tab\\there, newline above, quote \\" inside")
}""",
    },
    "string_concat": {
        "file": "concat.sc",
        "code": """use string

sfn main() {
    let name: String = "Silica"
    let version: String = "0.9.0"
    sprint(name + " v" + version)
    sprint(string.trim("   padded   "))
    sprint(string.ends_with(name, "ica"))
    sprint(string.contains(name, "lic"))
}""",
    },
    # ----------------------------------------------------------- collections
    "collections": {
        "file": "collections.sc",
        "code": """use collections

sfn main() {
    let nums: List = [5, 3, 9, 1]
    sprint(collections.sort(nums))
    sprint(collections.reverse(nums))
    sprint(collections.sum(nums))
    sprint(collections.index_of(nums, 9))

    let ages: Map = {"anita": 31, "rahul": 27}
    sprint(ages["anita"])
    sprint(has(ages, "rahul"))
    sprint(keys(ages))

    let bag: List = []
    push(bag, "apple")
    push(bag, "pear")
    sprint(bag)
}""",
    },
    # ---------------------------------------------------------------- module
    "json": {
        "file": "json_demo.sc",
        "code": """use json

sfn main() {
    let settings: Map = {"width": 80, "ratio": 1.5, "wrap": oui, "tags": ["a", "b"]}
    let text: String = json.stringify(settings)
    sprint(text)

    let parsed = json.parse(text)
    sprint(type_of(parsed))
    sprint(parsed["width"])
    sprint(json.stringify(parsed, 2))
}""",
    },
    "math": {
        "file": "math_demo.sc",
        "code": """use math

sfn main() {
    sprint(math.abs(-17))
    sprint(math.min(3, 8))
    sprint(math.max(3, 8))
    sprint(math.sqrt(81.0))
    sprint(math.pow(2.0, 10.0))
    sprint(math.floor(3.99))
    sprint(math.ceil(3.01))
    sprint(math.round(2.5))
    sprint(math.pi)
}""",
    },
    # ------------------------------------------------------------------- cli
    "cli_program": {
        "file": "greet.sc",
        "code": """sfn main() {
    dit("your name: ")
    let name: String = input("")
    sprint("Hello, " + name)
}""",
        "skip_run": True,
        "note": "reads stdin",
    },
}

# ---------------------------------------------- snippets used inside docs
SNIPPETS.update({
    "creator_card": {
        "file": "creator.sc",
        "code": """sfn main() {
    let creator: String = "Umaiz Sufiyan"
    let project: String = "Silica"
    sprint(project + " by " + creator)
    sprint("MIT licensed, built in the open")
}""",
    },
    "structure": {
        "file": "structure.sc",
        "code": """use string

const version: String = "0.9.0"

sfn greet(name: String) -> String {
    ret "Hello, " + name
}

sfn main() {
    sprint(greet("Silica"))
    sprint(version)
}""",
    },
    "literals": {
        "file": "literals.sc",
        "code": """sfn main() {
    let items: List = [1, 2, 3]
    let record: Map = {"language": "Silica", "version": "0.9.0"}
    let first: Int = items[0]
    let version: String = record["version"]
    sprint(first)
    sprint(version)
}""",
    },
    "while_loop": {
        "file": "while.sc",
        "code": """sfn main() {
    let n: Int = 5
    tant n > 0 {
        dit(n)
        dit(" ")
        n = n - 1
    }
    sprint("")
}""",
    },
    "halt_demo": {
        "file": "halt.sc",
        "code": """sfn main() {
    sprint("before")
    halt(3)
    sprint("never printed")
}""",
        "expect_exit": 3,
    },
    "divide": {
        "file": "divide.sc",
        "code": """sfn divide(a: Float, b: Float) -> Float {
    si b == 0.0 {
        sprint("cannot divide by zero")
        ret 0.0
    }
    ret a / b
}

sfn main() {
    sprint(divide(9.0, 2.0))
    sprint(divide(1.0, 0.0))
}""",
    },
    "unit_demo": {
        "file": "unit.sc",
        "code": """sfn noop() {
}

sfn main() {
    let nothing: Unit = noop()
    sprint(type_of(nothing))
}""",
    },
    "core_demo": {
        "file": "core.sc",
        "code": """sfn main() {
    let items: List = [1, 2, 3]
    sprint(type_of(items))
    sprint(len(items))
    sprint(str(42) + "!")
    sprint(has(items, 2))
}""",
    },
    "const_error": {
        "file": "const.sc",
        "code": """sfn main() {
    const x: Int = 1
    x = 2
}""",
        "expect_error": "cannot assign to 'x'",
    },
    "arity_error": {
        "file": "arity.sc",
        "code": """sfn add(a: Int, b: Int) -> Int {
    ret a + b
}

sfn main() {
    sprint(add(1))
}""",
        "expect_error": "expects 2 argument(s)",
    },
    "zero_error": {
        "file": "zero.sc",
        "code": """sfn main() {
    let a: Int = 1
    let b: Int = 0
    sprint(a / b)
}""",
        "expect_error": "division by zero",
    },
})

SNIPPETS.update({
    # ------------------------------------------------- 0.9.2: structs
    "struct_basic": {
        "file": "structs.sc",
        "code": """struct Point {
    x: Int
    y: Int
}

sfn main() {
    let p = Point(x: 3, y: 4)
    sprint(p.x)
    sprint(p)
    p.x = 10
    sprint(p.x)
}""",
    },
    "struct_nested": {
        "file": "nested.sc",
        "code": """struct Vec {
    x: Int
    y: Int
}

struct Box {
    corner: Vec
    label: String
}

sfn main() {
    let b = Box(corner: Vec(x: 1, y: 2), label: "origin")
    sprint(b.corner.x)
    b.corner.x = 10
    sprint(b)
}""",
    },
    "struct_fn": {
        "file": "struct_fn.sc",
        "code": """struct Point {
    x: Int
    y: Int
}

sfn length_squared(p: Point) -> Int {
    ret p.x * p.x + p.y * p.y
}

sfn main() {
    let a = Point(3, 4)
    sprint(length_squared(a))
    let b = Point(x: 3, y: 4)
    sprint(a == b)
}""",
    },
    # ------------------------------------------------- 0.9.1: colours
    "colors_demo": {
        "file": "colors.sc",
        "code": """use colors

sfn main() {
    let accent = colors.parse("#8B9BFF")
    sprint(colors.hex(accent))
    sprint(colors.contrast("#8B9BFF", "#0B1020"))
    sprint(colors.passes("#8B9BFF", "#0B1020", "AA", oui))
    let scale = colors.palette("#8B9BFF", [50, 500, 950])
    sprint(scale)
    sprint(colors.css(accent, "hex"))
}""",
    },
})

# Defaults: stdin or capability-bound snippets are checked but not executed.
for _entry in SNIPPETS.values():
    _entry.setdefault("skip_run", False)
    _entry.setdefault("expect_error", None)
    _entry.setdefault("expect_exit", 0)
