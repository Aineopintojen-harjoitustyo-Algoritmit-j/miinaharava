#!/bin/bash
OPTIONS="-b -a -u"
let COUNT=1000
let WINS=0
for ((i=0;i<COUNT;i++)); do
	python3 miinaharava $OPTIONS && let WINS++;
done
let PERCENT=100*WINS/COUNT
echo -ne "\n\n## Voittoja $WINS/$COUNT ($PERCENT%)\n\n"
