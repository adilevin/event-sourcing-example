"""
Script placeholder for debugging purposes
"""
from bank import Bank
Bank.reset()

B = Bank()
print "Creating 'adi' account"
B.create_account("adi")
B.deposit("adi", 10)
B.deposit("adi", 10)
B.deposit("adi", 10)
B.withdraw("adi", 25)
