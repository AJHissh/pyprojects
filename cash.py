# Gets user input for change amount requested
while True:
    try:
        CashOwed = float('Enter Change Amount: ')
        if CashOwed < 0:
            print('Please try again')
        else:
            break
    except ValueError:
        print('Error')

quarter = 0.25
dime = 0.10
nickel = 0.05
penny = 0.01

iteration = 0

denominations = [quarter, dime, nickel, penny]

# coin will subtract from CashOwed until CashOwed is less than coin, then moves to the next coin value for next iterations
for coin in denominations:
    while CashOwed >= coin:
        CashOwed = CashOwed - coin
        CashOwed = round(CashOwed, 2)
        iteration += 1
print(iteration)






