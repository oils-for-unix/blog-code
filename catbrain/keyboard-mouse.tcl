#!/usr/bin/env wish

# Create a canvas widget
pack [canvas .c -background lightblue -width 400 -height 300]

# Create a text widget for output messages
pack [text .t -width 40 -height 5 -wrap word]

# Function to handle mouse clicks
proc handle_mouse_click {x y} {
    .t insert end "Mouse clicked at coordinates: $x, $y\n"
    .t see end
    
    # Draw a small circle where the mouse was clicked
    .c create oval [expr $x-5] [expr $y-5] [expr $x+5] [expr $y+5] -fill red -outline black
}

# Function to handle keyboard events
proc handle_key_press {key} {
    .t insert end "Key pressed: $key\n"
    .t see end
}

# Bind mouse click event to the canvas
bind .c <Button-1> {handle_mouse_click %x %y}

# Bind keyboard events to the main window
bind . <Key> {handle_key_press %K}

# Add initial instructions
.t insert end "Click on the blue canvas or press any key to see events.\n"

# Add a label with instructions
pack [label .l -text "Click on the canvas or press keys to generate events"]
