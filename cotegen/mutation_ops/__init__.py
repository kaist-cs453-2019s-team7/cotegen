compare_mutation = {
    '<': '<=',
    '<=': '<',
    '>': '>=',
    '>=': '>',
    '==': '!=',
    '!=': '==',
    '<>': '==',
}

and_or_mutation = {
    'and': 'or',
    'or': 'and'
}

operator_mutation = {
    '+': '-',
    '-': '+',
    '*': '/',
    '/': '*',
    '//': '/',
    '%': '/',
    '<<': '>>',
    '>>': '<<',
    '&': '|',
    '|': '&',
    '^': '&',
    '**': '*',
    '~': '',

    '+=': '-=',
    '-=': '+=',
    '*=': '/=',
    '/=': '*=',
    '//=': '/=',
    '%=': '/=',
    '<<=': '>>=',
    '>>=': '<<=',
    '&=': '|=',
    '|=': '&=',
    '^=': '&=',
    '**=': '*=',
    '~=': '=',
}

keyword_mutation = {
    'not': '',
    'is': 'is not',  # this will cause "is not not" sometimes, so there's a hack to fix that later
    'in': 'not in',
    'break': 'continue',
    'continue': 'break',
    'True': 'False',
    'False': 'True',
}
