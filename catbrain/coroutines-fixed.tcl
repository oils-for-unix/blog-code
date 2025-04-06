#!/usr/bin/env wish

package require Tcl 8.6

# Create the main window layout
wm title . "Tcl Coroutines Demo"
wm minsize . 500 400

# Create two frames for the text widgets
frame .f1 -borderwidth 2 -relief groove
frame .f2 -borderwidth 2 -relief groove

# Create labels for each text widget
label .f1.label -text "Timer Output:"
label .f2.label -text "Keyboard Input:"

# Create two text widgets
text .f1.t -width 40 -height 10 -wrap word -yscrollcommand ".f1.scroll set"
text .f2.t -width 40 -height 10 -wrap word -yscrollcommand ".f2.scroll set"

# Add scrollbars
scrollbar .f1.scroll -orient vertical -command ".f1.t yview"
scrollbar .f2.scroll -orient vertical -command ".f2.t yview"

# Pack the widgets
pack .f1 -side top -fill both -expand yes -padx 10 -pady 5
pack .f2 -side top -fill both -expand yes -padx 10 -pady 5

pack .f1.label -side top -anchor w
pack .f1.scroll -side right -fill y
pack .f1.t -side left -fill both -expand yes

pack .f2.label -side top -anchor w
pack .f2.scroll -side right -fill y
pack .f2.t -side left -fill both -expand yes

# Make the second text widget automatically receive keyboard focus
focus .f2.t

# Timer coroutine procedure - true asynchronous version
proc timerProc {} {
    set counter 1
    
    # Helper procedure for yielding and returning after a delay
    proc asyncYield {ms} {
        after $ms [info coroutine]
        return -level 0 [yield]
    }
    
    while {1} {
        .f1.t insert end "Timer tick: $counter\n"
        .f1.t see end
        incr counter
        
        # This is the key change - asynchronous yield that will resume after 1 second
        asyncYield 1000
    }
}

# Keyboard coroutine procedure
proc keyboardProc {} {
    while {1} {
        set key [yield]
        .f2.t insert end "Key pressed: $key\n"
        .f2.t see end
    }
}

# Create the coroutines
coroutine timer timerProc
coroutine keyboard keyboardProc

# No need for the resumeTimer procedure anymore, the timer coroutine
# schedules itself to be called after the delay

# Bind keyboard events to pass to the keyboard coroutine
bind . <Key> {
    if {[string length %K] == 1 || [string match F* %K] || 
        [string match Return %K] || [string match BackSpace %K] ||
        [string match space %K] || [string match Tab %K]} {
        keyboard %K
    }
}

# Add some initial text
.f1.t insert end "Timer will update every second...\n\n"
.f2.t insert end "Press keys to see them recorded here...\n\n"

# Add a quit button
button .quit -text "Quit" -command exit
pack .quit -side bottom -pady 10
