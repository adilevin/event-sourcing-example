"""
Script placeholder for debugging purposes
"""
import bank_factory
from bank import NotEnoughMoneyForWithdrawalException

B = bank_factory.create_bank_with_mongodb_event_store(
    host="localhost", port=27017, db_name="bank_event_store", reset=True)

print "Ed creates account and deposits 100 + 200 + 300"
B.create_account("Ed")
for amount in [10, 20, 30]:
    B.deposit("Ed", amount)
print "Ed withdraws 10 + 20 + 30"
for amount in [10, 20, 30]:
    B.withdraw("Ed", amount)
print "Jen creates account and deposits 50 + 100"
B.create_account("Jen")
for amount in [50, 100]:
    B.deposit("Jen", amount)
print "Jen transfers 80 to Ed"
B.transfer(from_account='Jen', to_account='Ed', amount=100)
print "Jen tries to withdraw 100"
try:
    B.withdraw("Jen", 100)
    print "Success"
except NotEnoughMoneyForWithdrawalException:
    print "Sorry, Jen: You only have %d. This is your balance:" % B.get_balance("Jen")
print B.get_statement("Jen")
print "Use B"
