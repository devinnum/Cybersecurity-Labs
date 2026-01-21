#!/bin/bash

echo The name of this cryptocurrency is:
./cryptomoney.sh name
echo Creation of the genesis block
./cryptomoney.sh genesis
echo Creating a wallet for alice into alice.wallet.txt
./cryptomoney.sh generate alice.wallet.txt
export alice=`./cryptomoney.sh address alice.wallet.txt`
echo alice.wallet.txt wallet signature: $alice
echo funding alice wallet with 100
./cryptomoney.sh fund $alice 100 01-alice-funding.txt
echo Creating a wallet for bob into alice.wallet.txt
./cryptomoney.sh generate bob.wallet.txt
export bob=`./cryptomoney.sh address bob.wallet.txt`
echo bob.wallet.txt wallet signature: $bob
echo funding bob wallet with 100
./cryptomoney.sh fund $bob 100 02-bob-funding.txt
echo transfering 12 from alice to bob
./cryptomoney.sh transfer alice.wallet.txt $bob 12 03-alice-to-bob.txt
echo transfering 2 from bob to alice
./cryptomoney.sh transfer bob.wallet.txt $alice 2 04-bob-to-alice.txt
echo verifying the last four transactions
./cryptomoney.sh verify alice.wallet.txt 01-alice-funding.txt
./cryptomoney.sh verify bob.wallet.txt 02-bob-funding.txt
./cryptomoney.sh verify alice.wallet.txt 03-alice-to-bob.txt
./cryptomoney.sh verify bob.wallet.txt 04-bob-to-alice.txt
echo displaying the mempool
cat mempool.txt
echo checking the balance of both alice and bob
./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
echo mining the block with prefix of 2
./cryptomoney.sh mine 2
./cryptomoney.sh generate devinn.wallet.txt
export devinn=`./cryptomoney.sh address devinn.wallet.txt`
echo devinn.wallet.txt wallet signature: $devinn
./cryptomoney.sh fund $devinn 10000000 05-devinn-funding.txt
./cryptomoney.sh transfer devinn.wallet.txt $alice 1000 06-devinn-to-alice.txt
./cryptomoney.sh transfer devinn.wallet.txt $bob 750 07-devinn-to-bob.txt
./cryptomoney.sh verify devinn.wallet.txt 05-devinn-funding.txt
./cryptomoney.sh verify devinn.wallet.txt 06-devinn-to-alice.txt
./cryptomoney.sh verify devinn.wallet.txt 07-devinn-to-bob.txt
./cryptomoney.sh mine 2
./cryptomoney.sh transfer bob.wallet.txt $alice 10 08-bob-to-alice.txt
./cryptomoney.sh transfer devinn.wallet.txt $bob 150 09-devinn-to-bob.txt
./cryptomoney.sh transfer alice.wallet.txt $devinn 100 10-alice-to-devinn.txt
./cryptomoney.sh verify bob.wallet.txt 08-bob-to-alice.txt
./cryptomoney.sh verify devinn.wallet.txt 09-devinn-to-bob.txt
./cryptomoney.sh verify alice.wallet.txt 10-alice-to-devinn.txt
./cryptomoney.sh balance $devinn
./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
./cryptomoney.sh mine 2
./cryptomoney.sh transfer bob.wallet.txt $alice 1000 11-bob-to-alice.txt
./cryptomoney.sh transfer alice.wallet.txt $devinn 1800 12-alice-to-devinn.txt
./cryptomoney.sh transfer alice.wallet.txt $devinn 300 13-alice-to-devinn.txt
./cryptomoney.sh transfer alice.wallet.txt $bob 100 14-alice-to-bob.txt
./cryptomoney.sh verify bob.wallet.txt 11-bob-to-alice.txt
./cryptomoney.sh verify alice.wallet.txt 12-alice-to-devinn.txt
./cryptomoney.sh verify alice.wallet.txt 13-alice-to-devinn.txt
./cryptomoney.sh verify alice.wallet.txt 14-alice-to-bob.txt
./cryptomoney.sh mine 2
./cryptomoney.sh balance $devinn
./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
./cryptomoney.sh generate madelyn.wallet.txt
export madelyn=`./cryptomoney.sh address madelyn.wallet.txt`
./cryptomoney.sh fund $madelyn 10000000 15-madelyn-funding.txt
./cryptomoney.sh transfer devinn.wallet.txt $madelyn 10000000 16-devinn-to-madelyn.txt
./cryptomoney.sh verify madelyn.wallet.txt 15-madelyn-funding.txt
./cryptomoney.sh verify devinn.wallet.txt 16-devinn-to-madelyn.txt
./cryptomoney.sh mine 2
echo Madelyns Balance:
./cryptomoney.sh balance $madelyn
echo validating the cryptocurrency chain
./cryptomoney.sh validate