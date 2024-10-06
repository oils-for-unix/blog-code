#!/usr/bin/env python3
#
# Demo from Claude AI that doesn't run

import re

def validate_xml(xml):
    # Remove comments
    xml = re.sub(r'<!--[\s\S]*?-->', '', xml)

    # Check for root element - BUG
    if not re.match(r'^\s*<[^?].*>[\s\S]*</\1>\s*$', xml):
        return False

    # Check for proper nesting and closing tags
    stack = []
    for tag in re.findall(r'</?[\w:-]+', xml):
        if tag.startswith('</'):
            if not stack or stack.pop() != tag[2:]:
                return False
        else:
            stack.append(tag[1:])

    if stack:
        return False

    # Check for quoted attributes
    if re.search(r'<[\w:-]+[^>]*\s+\w+\s*=\s*[^"\']', xml):
        return False

    return True

# Test the validator
xml_samples = [
    '<root><child>Content</child></root>',
    '<root><child>Content</child><child>More</child></root>',
    '<root><child>Content</child><child>More</child>',
    '<root><child attr="value">Content</child></root>',
    '<root><child attr=value>Content</child></root>',
]

for i, xml in enumerate(xml_samples, 1):
    print(f"Sample {i} is {'valid' if validate_xml(xml) else 'invalid'} XML")
