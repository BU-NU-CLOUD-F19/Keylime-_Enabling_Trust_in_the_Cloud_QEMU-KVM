#!/bin/bash
# Send curl GET request to provider verifier
test_verifier(){
  echo -e "Running request"
  
  
  	curl "http://11.0.0.22:8881/verifier?nonce=1&mask=0x108000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=2&mask=0x208000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=33&mask=0x308000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=4&mask=0x408000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=5&mask=0x508000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=6&mask=0x108000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=7&mask=0x208000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=83&mask=0x308000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=9&mask=0x408000&vmask=0x808000"&
  	curl "http://11.0.0.22:8881/verifier?nonce=10&mask=0x508000&vmask=0x808000"&
  
  
 }

test_verifier 

wait
echo "All done"
