import numpy as np


def gen_demand(l_demand=1, u_demand=4, size=20):
    """
    Generate demand
    """
    return np.random.randint(low=l_demand, high=u_demand + 1, size=size + 1)


def gen_delivery_time(lower_time, upper_time):
    """
    Generates delivery time
    """
    return np.random.randint(low=lower_time, high=upper_time)


def inventory_model(
    n_weeks=20,
    lower_demand=1,
    upper_demand=4,
    l_order_time=1,
    u_order_time=3,
    f_oc=30,
    f_hc=2,
    f_sc=20,
    f_roq=6,
    f_rop=3,
    i_stock=6,
):
    """
    Main inventory function
    """
    # n_weeks = 20
    # lower_demand = 1
    # upper_demand = 4

    FIXED_ORDER_COST = f_oc
    FIXED_HOLDING_COST = f_hc
    FIXED_STOCKOUT_COST = f_sc
    FIXED_REORDER_QUANTITY = f_roq

    # initial stock
    INITIAL_STOCK = i_stock

    # np.random.seed(72)
    # np.random.seed(108)

    stock = np.zeros(shape=n_weeks, dtype=int)
    stock[0] = INITIAL_STOCK

    order_cost = np.zeros(shape=n_weeks, dtype=int)
    holding_cost = np.zeros(shape=n_weeks, dtype=int)
    stock_out_cost = np.zeros(shape=n_weeks, dtype=int)
    total_cost = np.zeros(shape=n_weeks, dtype=int)

    # Generate demand
    demand = gen_demand(l_demand=lower_demand, u_demand=upper_demand, size=n_weeks)
    # np.random.randint(low=1, high=4 + 1, size=21)
    print(f"System Demand: \n{demand}")

    # Reorder time
    reorder = np.full(shape=n_weeks, fill_value=99)
    FIXED_REORDER_POINT = f_rop

    for i in range(n_weeks):
        if demand[i] < stock[i]:
            print("Demand is less than Stock")
            new_stock = stock[i] - demand[i]

            # Update stock available for the next week
            try:
                stock[i + 1] += new_stock
            except IndexError:
                print("index Out of Bounds - update stock in advance - demand<stock")

            weekly_stock_out_cost = 0  # All demand fulfilled

            if (new_stock <= FIXED_REORDER_POINT) and (reorder[i] == 99):
                reorder[i] = 1  # Order will get placed this week

                weekly_order_cost = FIXED_ORDER_COST
                weekly_delivery_time = gen_delivery_time(
                    lower_time=l_order_time, upper_time=u_order_time
                )

                print(f"Weekly delivery time: {weekly_delivery_time} - Week {i}")

                # Add stock in-advance
                try:
                    stock[i + weekly_delivery_time] += FIXED_REORDER_QUANTITY
                except IndexError:
                    print("Index Out of Bounds - Replenish - demand<stock")

                # Block further reorders
                for j in range(i + 1, i + weekly_delivery_time + 1):
                    try:
                        reorder[j] = 0
                    except IndexError:
                        print("Index Out of Bounds - block reorder - demand<stock")
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

            # try:
            #     stock[i + 1] += new_stock
            # except IndexError:
            #     print("Index Out of bounds - Add stock in advance - demand>stock")

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

                weekly_delivery_time = gen_delivery_time(
                    lower_time=l_order_time, upper_time=u_order_time
                )

                print(f"Weekly delivery time: {weekly_delivery_time} - Week {i}")

                # Add stock in-advance
                try:
                    stock[i + weekly_delivery_time] += FIXED_REORDER_QUANTITY
                except IndexError:
                    print("Out of Bounds - add stock - demand>stock")

                # Block further reorders
                for j in range(i + 1, i + weekly_delivery_time + 1):
                    try:
                        reorder[j] = 0
                    except IndexError:
                        print("index out of bounds - block reorder - demand>stock")

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

    return {
        "demand": demand,
        "stock_detail": stock,
        "reorder_point": reorder,
        "order_cost": order_cost,
        "holding_cost": holding_cost,
        "stockout_cost": stock_out_cost,
        "total_cost": total_cost,
    }


if __name__ == "__main__":
    inventory_model()
