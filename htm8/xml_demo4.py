#!/usr/bin/env python3
#
# "please do it in a single pass, reading the input exactly once, with a lexer producing different tokens"

import re
from enum import Enum, auto

class TokenType(Enum):
    TAG_OPEN = auto()
    TAG_CLOSE = auto()
    ATTR_NAME = auto()
    ATTR_VALUE = auto()
    TEXT = auto()
    COMMENT = auto()
    CDATA = auto()
    ENTITY = auto()

class XMLValidator:
    def __init__(self):
        self.token_specs = [
            ('COMMENT', r'<!--[\s\S]*?-->'),
            ('CDATA', r'<!\[CDATA\[[\s\S]*?\]\]>'),
            ('TAG_OPEN', r'</?[\w:.-]+'),
            ('TAG_CLOSE', r'/?>'),
            ('ATTR_NAME', r'\s+([\w:.-]+)'),
            ('ATTR_VALUE', r'=\s*("[^"]*"|\'[^\']*\')'),
            ('ENTITY', r'&[#\w]+;'),
            ('TEXT', r'[^<&]+')
        ]
        self.tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specs)
        self.get_token = re.compile(self.tok_regex).match
        self.stack = []
        self.in_tag = False

    def tokenize(self, text):
        pos = 0
        while True:
            match = self.get_token(text, pos)
            if not match:
                if pos != len(text):
                    raise ValueError(f"Unexpected character '{text[pos]}' at position {pos}")
                break
            pos = match.end()
            token_type = match.lastgroup
            yield TokenType[token_type], match.group(token_type)

    def validate(self, xml):
        for token_type, token_value in self.tokenize(xml):
            if token_type == TokenType.TAG_OPEN:
                if token_value.startswith('</'):
                    if not self.stack or self.stack.pop() != token_value[2:]:
                        return False
                else:
                    self.stack.append(token_value[1:])
                self.in_tag = True
            elif token_type == TokenType.TAG_CLOSE:
                if token_value == '/>':
                    self.stack.pop()
                self.in_tag = False
            elif token_type == TokenType.ATTR_NAME:
                if not self.in_tag:
                    return False
            elif token_type == TokenType.ATTR_VALUE:
                if not self.in_tag:
                    return False
            elif token_type == TokenType.TEXT:
                if '<' in token_value or '>' in token_value:
                    return False
            elif token_type == TokenType.ENTITY:
                if not token_value.startswith('&#') and token_value not in ('&lt;', '&gt;', '&amp;', '&apos;', '&quot;'):
                    return False
        return len(self.stack) == 0

# Test the validator
xml_samples = [
    '<root><child>Content</child></root>',
    '<root><child>Content with &lt;brackets&gt;</child></root>',
    '<root><child>Invalid char <</child></root>',
    '<root><child>Valid numeric entity &#65;</child></root>',
    '<root><child>Invalid entity &invalid;</child></root>',
    '<root attribute="value&quot;quoted&quot;">Content</root>',
    '<root><![CDATA[<raw content & special characters>]]></root>',
    '<root>Mix of valid &lt;brackets&gt; and invalid &</root>',
    '<root><self-closing/></root>',
    '<!-- comment --><root>Content</root>',
    '<ns:root xmlns:ns="http://example.com"><ns:child>Content</ns:child></ns:root>',
]

validator = XMLValidator()
for i, xml in enumerate(xml_samples, 1):
    try:
        is_valid = validator.validate(xml)
        print(f"Sample {i} is {'valid' if is_valid else 'invalid'} XML")
    except ValueError as e:
        print(f"Sample {i} is invalid XML: {str(e)}")
