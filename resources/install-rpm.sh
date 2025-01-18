#!/bin/bash
for i in `ls /tmp/rpm/`;
do
  echo "rpm -i --nodeps" /tmp/rpm/$i|bash
done
