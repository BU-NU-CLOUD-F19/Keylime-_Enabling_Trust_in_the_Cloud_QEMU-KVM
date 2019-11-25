#!/bin/bash
# Send curl GET request to provider verifier
test_verifier(){
  echo -e "Running request"
  for i in {1..5}
  do
  	curl "http://10.0.0.11:8881/verifier?nonce=7$i98ea9d&mask=0x408000&vmask=0x808000"
  	echo "curl http://10.0.0.11:8881/verifier?nonce=7$i98ea9d&mask=0x408000&vmask=0x808000"
  done
 }

test_verifier 

wait
echo "All done"
