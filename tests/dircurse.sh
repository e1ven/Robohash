function dircurse()
{
    local count
    local i
    local newfile
    echo "Entering Dircurse for " $1
    count=0
    for i in `ls -U $1`
    do
        newfile=$1/`printf %03d $count`#$i 
        mv $1/$i $newfile
        count=`expr $count + 1`
        if [ -d $newfile ]
        then
            echo "Dircursing $newfile"
            dircurse $newfile
        fi
    done
}

if [ $# -lt 1 ]
    then
        echo "Usage: $0 directory"
        exit
    fi
dircurse $1
