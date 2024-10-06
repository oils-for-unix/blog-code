#!/usr/bin/env python3
#
# After asking for self-closing tags
#
# Now it does not validate special characters!

import re

def validate_xml(xml):
    # Remove comments
    xml = re.sub(r'<!--[\s\S]*?-->', '', xml)

    # Check for root element
    if not re.match(r'^\s*<([^?/\s>]+)[^>]*>[\s\S]*</\1>\s*$', xml):
        return False

    # Check for proper nesting, closing tags, and self-closing tags
    stack = []
    for tag in re.finditer(r'<(?:/?)([^\s>/]+)([^>]*)>', xml):
        tag_name, attributes = tag.groups()
        if tag.group().startswith('</'):
            if not stack or stack.pop() != tag_name:
                return False
        else:
            if not attributes.endswith('/'):
                stack.append(tag_name)

    if stack:
        return False

    # Check for quoted attributes
    if re.search(r'<[^>]+\s+\w+\s*=\s*[^"\'][^>]*>', xml):
        return False

    return True

# Test the validator
xml_samples = [
    '<root><child>Content</child></root>',
    '<root><child>Content</child><child>More</child></root>',
    '<root><child>Content</child><child>More</child>',
    '<root><child attr="value">Content</child></root>',
    '<root><child attr=value>Content</child></root>',
    '<?xml version="1.0"?><root>Content</root>',
    '<root/>',
    '<ns:root xmlns:ns="http://example.com"><ns:child>Content</ns:child></ns:root>',
    '<root><self-closing-tag/></root>',
    '<root><self-closing-tag with="attribute"/></root>',
    '<root><invalid-self-closing-tag></root>',
    '<root><mixed><self-closing-tag/><normal>Content</normal></mixed></root>'
]

for i, xml in enumerate(xml_samples, 1):
    print(f"Sample {i} is {'valid' if validate_xml(xml) else 'invalid'} XML")

