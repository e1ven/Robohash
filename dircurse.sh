function dircurse()
{
    count=0
    cd $1
    for i in `ls -U`
    do
        echo mv $i $count#$i
        count=`expr $count + 1`
        if [ -d $i ]
        then
            dircurse $i    
        fi
    done
}

if [ $? -lt 1 ]
    then
    echo "Usage: $0 directory"
    fi
dircurse $1
