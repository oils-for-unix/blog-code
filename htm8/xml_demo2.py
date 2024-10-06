#!/usr/bin/env python3
#
# After asking for correct regex

import re

def validate_xml(xml):
    # Remove comments
    xml = re.sub(r'<!--[\s\S]*?-->', '', xml)
    
    # Check for root element
    if not re.match(r'^\s*<([^?/\s>]+)[^>]*>[\s\S]*</\1>\s*$', xml):
        return False
    
    # Check for proper nesting and closing tags
    stack = []
    for tag in re.finditer(r'</?([^\s>/]+)', xml):
        tag_name = tag.group(1)
        if tag.group().startswith('</'):
            if not stack or stack.pop() != tag_name:
                return False
        else:
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
]

for i, xml in enumerate(xml_samples, 1):
    print(f"Sample {i} is {'valid' if validate_xml(xml) else 'invalid'} XML")

