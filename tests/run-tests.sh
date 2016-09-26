#!/bin/bash

if which colordiff >/dev/null 2>&1; then
    DIFF=colordiff
else
    DIFF=diff
fi

cd $(dirname ${BASH_SOURCE[0]})

status=0
for file in *.lll; do
    expected=$(cat "$file" | grep -oE '# => .*' | cut -c6-)
    actual=$(../lll.py $file 2>&1)

    if [ "$expected" = "$actual" ]; then
        echo "OK: $file"
    else
        echo "=================================================="
        echo "FAIL: $file"
        $DIFF -u --label "$file (expected)" --label "$file (actual)" <(echo "$expected") <(echo "$actual") # | tail -n +3
        echo "=================================================="
        status=1
    fi
done

exit $status
