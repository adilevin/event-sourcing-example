"""
Script placeholder for debugging purposes
"""
import bank_factory
from bank import NotEnoughMoneyForWithdrawalException

B = bank_factory.create_bank_with_mongodb_event_store(host="localhost", port=27017, db_name="bank_db", reset=True)

print "John creates account and deposits 10 + 20 + 30"
B.create_account("john")
for amount in [10, 20, 30]:
    B.deposit("john", amount)
print "John withdraws 1 + 2 + 3"
for amount in [1, 2, 3]:
    B.withdraw("john", amount)
print "Bella creates account and deposits 50 + 100"
B.create_account("bella")
for amount in [50, 100]:
    B.deposit("bella", amount)
print "Bella transfers 100 to John"
B.transfer(from_account='bella', to_account='john', amount=100)
print "Bella tries to withdraw 100"
try:
    B.withdraw("bella", 100)
    print "Success"
except NotEnoughMoneyForWithdrawalException:
    print "Sorry, Bella: You only have %d" % B.get_balance("bella")