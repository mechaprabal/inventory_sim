import numpy as np

# np.random.seed(72)
# np.random.seed(108)

n_weeks = 20
lower_demand = 1
upper_demand = 4

l_order_time = 1
u_order_time = 3

FIXED_ORDER_COST = 30
FIXED_HOLDING_COST = 2
FIXED_STOCKOUT_COST = 20
FIXED_REORDER_QUANTITY = 6

# initial stock
INITIAL_STOCK = 6

stock = np.zeros(shape=n_weeks + 1, dtype=int)
stock[0] = INITIAL_STOCK

order_cost = np.zeros(shape=n_weeks + 1, dtype=int)
holding_cost = np.zeros(shape=n_weeks + 1, dtype=int)
stock_out_cost = np.zeros(shape=n_weeks + 1, dtype=int)
total_cost = np.zeros(shape=n_weeks + 1, dtype=int)

# Generate demand
demand = np.random.randint(low=1, high=4 + 1, size=21)
print(f"System Demand: \n{demand}")

# Reorder time
reorder = np.full(shape=n_weeks + 1, fill_value=99)
reorder_point = 3


def gen_delivery_time(lower_time, upper_time):
    """
    Generates delivery time
    """
    return np.random.randint(low=lower_time, high=upper_time)


for i in range(n_weeks + 1):
    if demand[i] < stock[i]:
        print("Demand is less than Stock")
        new_stock = stock[i] - demand[i]

        # Update stock available for the next week
        try:
            stock[i + 1] += new_stock
        except IndexError:
            print("index Out of Bounds")

        weekly_stock_out_cost = 0  # All demand fulfilled

        if (new_stock <= reorder_point) and (reorder[i] == 99):
            reorder[i] = 1  # Order will get placed this week

            weekly_order_cost = FIXED_ORDER_COST
            weekly_delivery_time = gen_delivery_time(lower_time=1, upper_time=3)

            print(f"Weekly delivery time: {weekly_delivery_time} - Week {i}")

            # Add stock in-advance
            try:
                stock[i + weekly_delivery_time] += FIXED_REORDER_QUANTITY
            except IndexError:
                print("Index Out of Bounds")

            # Block further reorders
            for j in range(i + 1, i + weekly_delivery_time + 1):
                try:
                    reorder[j] = 0
                except IndexError:
                    print("Index Out of Bounds")
        else:
            # No order will be placed
            weekly_order_cost = 0

        # Cost calculations
        holding_cost[i] = new_stock * FIXED_HOLDING_COST
        order_cost[i] = weekly_order_cost
        stock_out_cost[i] = weekly_stock_out_cost

        total_cost[i] = holding_cost[i] + order_cost[i] + stock_out_cost[i]

    elif demand[i] >= stock[i]:
        print("demand is greater than stock")
        new_stock = 0

        try:
            stock[i + 1] += new_stock
        except IndexError:
            print("Index Out of bounds")

        unmet_demand = demand[i] - stock[i]

        weekly_stock_out_cost = FIXED_STOCKOUT_COST * unmet_demand
        stock_out_cost[i] = weekly_stock_out_cost

        # Nothing to hold in inventory
        holding_cost[i] = new_stock * FIXED_HOLDING_COST

        if reorder[i] == 99:
            # No active order
            reorder[i] = 1

            weekly_order_cost = FIXED_ORDER_COST
            order_cost[i] = weekly_order_cost

            weekly_delivery_time = gen_delivery_time(lower_time=1, upper_time=3)

            print(f"Weekly delivery time: {weekly_delivery_time} - Week {i}")

            # Add stock in-advance
            try:
                stock[i + weekly_delivery_time] += FIXED_REORDER_QUANTITY
            except IndexError:
                print("Out of Bounds")

            # Block further reorders
            for j in range(i + 1, i + weekly_delivery_time + 1):
                try:
                    reorder[j] = 0
                except IndexError:
                    print("index out of bounds")

        else:
            # No reorder
            weekly_order_cost = 0
            order_cost[i] = weekly_order_cost


print(f"System Stock:\n{stock}")
print(f"System Reorder:\n{reorder}")

print(f"order cost:\n{order_cost}")
print(f"holding cost:\n{holding_cost}")
print(f"Stock Out cost:\n{stock_out_cost}")
print(f"Total cost:\n{total_cost}")
