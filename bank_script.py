"""
Script placeholder for debugging purposes
"""
import bank_factory
from bank import NotEnoughMoneyForWithdrawalException

B = bank_factory.create_bank_with_mongodb_event_store(
    host="localhost", port=27017, db_name="bank_event_store", reset=True)

print "Eduard creates account and deposits 10 + 20 + 30"
B.create_account("Eduard")
for amount in [10, 20, 30]:
    B.deposit("Eduard", amount)
print "Eduard withdraws 1 + 2 + 3"
for amount in [1, 2, 3]:
    B.withdraw("Eduard", amount)
print "Bella creates account and deposits 50 + 100"
B.create_account("bella")
for amount in [50, 100]:
    B.deposit("bella", amount)
print "Bella transfers 100 to Eduard"
B.transfer(from_account='bella', to_account='Eduard', amount=100)
print "Bella tries to withdraw 100"
try:
    B.withdraw("bella", 100)
    print "Success"
except NotEnoughMoneyForWithdrawalException:
    print "Sorry, Bella: You only have %d" % B.get_balance("bella")

print "Use B"
