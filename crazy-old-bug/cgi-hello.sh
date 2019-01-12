#!/bin/bash

cat <<EOF
Content-type: text/html

<!DOCTYPE html>
<html>
  <head>
   <title>Hello</title>
  </head>
  <body>

  <h1>Hello</h1>
EOF


if [ "$REQUEST_METHOD" = "POST" ]; then
    echo "<p>POST</p>"
    if [[ "$CONTENT_LENGTH" -gt 0 ]]; then
        echo "<p>CONTENT_LENGTH=$CONTENT_LENGTH</p>"
        { 
           while read -r line; do
             echo "$line"
           done
        } > out.txt
        echo "<p>Wrote to out.txt</p>"
    fi
fi

cat <<EOF
  </body>
</html>
EOF
