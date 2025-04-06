#!/usr/bin/env wish

package require Tcl 8.6

# Create the main window layout
wm title . "Tcl Process Execution Demo"
wm minsize . 600 500

# Create frames for the widgets
frame .timer -borderwidth 2 -relief groove
frame .process -borderwidth 2 -relief groove
frame .controls -borderwidth 2 -relief groove

# Create labels for each text widget
label .timer.label -text "Timer Output:"
label .process.label -text "Process Execution Log:"

# Create text widgets with scrollbars
text .timer.t -width 40 -height 10 -wrap word -yscrollcommand ".timer.scroll set"
scrollbar .timer.scroll -orient vertical -command ".timer.t yview"

text .process.t -width 40 -height 15 -wrap word -yscrollcommand ".process.scroll set"
scrollbar .process.scroll -orient vertical -command ".process.t yview"

# Create entry for command and execute button
label .controls.label -text "Enter system command:"
entry .controls.entry -width 40
button .controls.execute -text "Execute" -command runSystemCommand

# Pack the widgets
pack .timer -side top -fill both -expand yes -padx 10 -pady 5
pack .process -side top -fill both -expand yes -padx 10 -pady 5
pack .controls -side top -fill x -padx 10 -pady 5

pack .timer.label -side top -anchor w
pack .timer.scroll -side right -fill y
pack .timer.t -side left -fill both -expand yes

pack .process.label -side top -anchor w
pack .process.scroll -side right -fill y
pack .process.t -side left -fill both -expand yes

pack .controls.label -side top -anchor w -pady 2
pack .controls.entry -side top -fill x -pady 2
pack .controls.execute -side top -pady 5

# Timer coroutine procedure with asynchronous yield
proc timerProc {} {
    set counter 1
    
    # Helper procedure for yielding and returning after a delay
    proc asyncYield {ms} {
        after $ms [info coroutine]
        return -level 0 [yield]
    }
    
    while {1} {
        .timer.t insert end "Timer tick: $counter\n"
        .timer.t see end
        incr counter
        
        # Asynchronous yield that will resume after 1 second
        asyncYield 1000
    }
}

# Create the timer coroutine
coroutine timer timerProc

# Function to get current time formatted
proc getCurrentTime {} {
    return [clock format [clock seconds] -format "%H:%M:%S"]
}

# Process execution coroutine
proc processExecProc {cmd} {
    set startTime [getCurrentTime]
    .process.t insert end "Process started at $startTime: $cmd\n"
    .process.t see end
    
    # Execute the command asynchronously
    set pipe [open "|$cmd" r]
    fconfigure $pipe -blocking 0
    
    # Set up fileevent to handle command completion
    fileevent $pipe readable [list processOutput $pipe $cmd $startTime]
}

# Handle process output and completion
proc processOutput {pipe cmd startTime} {
    # Check if there's data to read
    if {[eof $pipe]} {
        set endTime [getCurrentTime]
        .process.t insert end "Process completed at $endTime\n"
        .process.t insert end "--------------------------------------------\n"
        .process.t see end
        close $pipe
        return
    }
    
    # Read and display output
    if {[gets $pipe line] >= 0} {
        .process.t insert end "$line\n"
        .process.t see end
    }
}

# Function to run system command from the entry widget
proc runSystemCommand {} {
    set cmd [.controls.entry get]
    if {$cmd eq ""} {
        .process.t insert end "Error: No command entered\n"
        .process.t see end
        return
    }
    
    processExecProc $cmd
    .controls.entry delete 0 end
}

# Bind Enter key in entry to execute command
bind .controls.entry <Return> runSystemCommand

# Add initial text
.timer.t insert end "Timer will update every second...\n\n"
.process.t insert end "Enter a command and click Execute or press Enter\n"
.process.t insert end "--------------------------------------------\n"

# Add a quit button
button .quit -text "Quit" -command exit
pack .quit -side bottom -pady 10

# Set focus to the entry widget
focus .controls.entry
