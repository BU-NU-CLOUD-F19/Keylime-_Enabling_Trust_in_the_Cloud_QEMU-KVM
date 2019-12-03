#!/bin/bash
# Send curl GET request to provider verifier
test_verifier(){
  echo -e "Running request"
  
  
  	curl "http://11.0.0.22:8881/verifier?nonce=15&mask=0x108000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=25&mask=0x208000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=35&mask=0x308000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=45&mask=0x408000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=55&mask=0x508000&vmask=0x808000"&
  
 }

test_verifier 

wait
echo "All done"
