from flask import Flask, render_template, request
from inventory_sim import inventory_model

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

font = {"family": "Palatino Linotype", "weight": "bold", "size": 16}

mpl.rc("font", **font)
plt.style.use("ggplot")

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    """
    Homepage
    """

    if request.method == "POST":
        chart_gen = 1
        form_res = request.form

        if int(form_res.get("seed")) == 99:
            pass
        else:
            np.random.seed(int(form_res.get("seed")))

        sim_result_list = []
        for sim in range(int(form_res.get("nsim"))):
            sim_result = inventory_model(
                n_weeks=int(form_res.get("nweek")),
                lower_demand=int(form_res.get("ldemand")),
                upper_demand=int(form_res.get("udemand")),
                l_order_time=int(form_res.get("l_odtime")),
                u_order_time=int(form_res.get("u_odtime")),
                f_oc=int(form_res.get("ordercost")),
                f_hc=int(form_res.get("holdingcost")),
                f_sc=int(form_res.get("stockoutcost")),
                f_roq=int(form_res.get("roq")),
                f_rop=int(form_res.get("rop")),
                i_stock=int(form_res.get("istock")),
            )
            sim_result["nsim"] = int(sim) + 1
            # print(sim_result.get("total_cost"))
            sim_result_list.append(
                {
                    "sim_number": int(sim) + 1,
                    "sim_result": sim_result,
                }
            )

        # print(form_res)

        all_sim_fig, avg_tc_fig, avg_of_avg = system_stat(sim_res_list=sim_result_list)

        # Generate report
        gen_report(sim_result_list)

        return render_template(
            "home.html",
            result_dict=sim_result,
            cost=sim_result.get("total_cost"),
            chart_gen=chart_gen,
            avg_of_avg=avg_of_avg,
            # all_sim_fig=all_sim_fig,
            # avg_tc_fig=avg_tc_fig,
        )
    else:
        # basic Form load
        return render_template("home.html")


def system_stat(sim_res_list):
    """
    Draw system statistics
    """
    # total_cost = sim_res.get("total_cost")  # ndarray

    fig1, ax1 = plt.subplots()

    each_sim_avg_total_cost = []
    for sim in sim_res_list:
        total_cost = sim.get("sim_result").get("total_cost")
        each_sim_avg_total_cost.append(np.mean(total_cost))
        # print(total_cost)
        ax1.plot(
            range(len(total_cost)),
            total_cost,
            label=f"sim{sim.get('sim_number')}",
        )

    avg_of_avg = np.mean(each_sim_avg_total_cost)

    print(f"Average of Average: {avg_of_avg}")
    ax1.set_title("Weekly Total Cost")
    ax1.set_xlabel("Week Number")
    ax1.set_ylabel("Total Cost")

    ax1.set_xticks(np.arange(len(total_cost)))

    ax1.set_xlim(xmin=0)
    ax1.set_ylim(ymin=0)

    fig1.savefig("./static/total_cost.png", bbox_inches="tight", dpi=300)

    fig2, ax2 = plt.subplots()

    ax2.plot(each_sim_avg_total_cost, label="avg_tc")
    ax2.set_title("Weekly Average Total Cost")
    ax2.set_xlabel("Week Number")
    ax2.set_ylabel("Total Cost")
    ax2.set_xlim(xmin=0)
    ax2.set_ylim(ymin=0)

    fig2.savefig("./static/avg_total_cost.png", bbox_inches="tight", dpi=300)

    return fig1, fig2, avg_of_avg


def gen_report(all_sim_data):
    """
    Generate an excel report of all simulations
    """

    sim_data_df = []

    # print(pd.DataFrame.from_dict(all_sim_data))
    for individual_sim in all_sim_data:
        for key, value in individual_sim.items():
            if key == "sim_result":
                df = pd.DataFrame(
                    list(
                        zip(
                            value["demand"],
                            value["stock_detail"],
                            value["reorder_point"],
                            value["order_cost"],
                            value["holding_cost"],
                            value["stockout_cost"],
                            value["total_cost"],
                        )
                    ),
                    columns=[
                        "demand",
                        "stock_detail",
                        "reorder_point",
                        "order_cost",
                        "holding_cost",
                        "stockout_cost",
                        "total_cost",
                    ],
                )
                # Add n_sim
                df.loc[:, "nsim"] = value["nsim"]
                # print(df)
                sim_data_df.append(df)

    pd.concat(sim_data_df).to_csv("./static/all_sim_report.csv", index=False)

    # print(pd.DataFrame.from_dict(sim_data_df))

    # print(key)
    # print("\n", sim_data)

    return


if __name__ == "__main__":
    app.run(debug=True)
