from argparse import ArgumentParser

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gdp_rename = {
    "Afghanistan, Islamic Republic of": "Afghanistan",
    "Armenia, Republic of": "Armenia",
    "Aruba, Kingdom of the Netherlands": "Aruba",
    "Azerbaijan, Republic of": "Azerbaijan",
    "Bahrain, Kingdom of": "Bahrain",
    "Belarus, Republic of": "Belarus",
    "China, People\'s Republic of": "China",
    "Comoros, Union of the": "Comoros",
    "Congo, Democratic Republic of the": "Democratic Republic of the Congo",
    "Croatia, Republic of": "Croatia",
    "Egypt, Arab Republic of": "Egypt",
    "Eritrea, The State of": "Eritrea",
    "Estonia, Republic of": "Estonia",
    "Eswatini, Kingdom of": "Eswatini",
    "Ethiopia, The Federal Democratic Republic of": "Ethiopia",
    "Fiji, Republic of": "Fiji",
    "Gambia, The": "Gambia",
    "Hong Kong Special Administrative Region, People\'s Republic of China": "Hong Kong",
    "Iran, Islamic Republic of": "Iran",
    "Kazakhstan, Republic of": "Kazakhstan",
    "Korea, Republic of": "South Korea",
    "Lao People\'s Democratic Republic": "Lao",
    "Latvia, Republic of": "Latvia",
    "Lesotho, Kingdom of": "Lesotho",
    "Liechtenstein, Principality of": "Liechtenstein",
    "Lithuania, Republic of": "Lithuania",
    "Macao Special Administrative Region, People\'s Republic of China": "Macao",
    "Madagascar, Republic of": "Madagascar",
    "Mauritania, Islamic Republic of": "Mauritania",
    "Moldova, Republic of": "Moldova",
    "Mozambique, Republic of": "Mozambique",
    "Netherlands, The": "Netherlands",
    "North Macedonia, Republic of": "North Macedonia",
    "Palau, Republic of": "Palau",
    "Poland, Republic of": "Poland",
    "Slovenia, Republic of": "Slovenia",
    "São Tomé and Príncipe, Democratic Republic of": "São Tomé and Príncipe",
    "Taiwan Province of China": "Taiwan",
    "Tajikistan, Republic of": "Tajikistan",
    "Tanzania, United Republic of": "Tanzania",
    "Timor-Leste, Democratic Republic of": "Timor-Leste",
    "Türkiye, Republic of": "Türkiye",
    "Uzbekistan, Republic of": "Uzbekistan",
    "Venezuela, República Bolivariana de": "Venezuela",
    "Yemen, Republic of": "Yemen",
}

def gdp():
    """
    GDP for all countries in USD billions
    """
    df = pd.read_csv("./data/gdp.csv", low_memory=False)
    df = df[["COUNTRY", "INDICATOR"] + [str(y) for y in range(1980, 2024)]]
    df = df[df["INDICATOR"] == "Gross domestic product (GDP), Current prices, US dollar"]
    df = df.rename(columns={"COUNTRY": "country"})
    df["country"] = df["country"].replace(gdp_rename)
    df = df.melt(
        id_vars=["country"],
        value_vars=[str(y) for y in range(1980, 2024)],
        var_name="year",
        value_name="gdp"
    )
    return df

def ghg():
    df = pd.read_csv("./data/emissions.csv")
    df = df[["Country"] + [str(y) for y in range(1980, 2024)]]
    df = df.rename(columns={"Country": "country"})
    df = df.melt(
        id_vars=["country"],
        value_vars=[str(y) for y in range(1980, 2024)],
        var_name="year",
        value_name="ghg"
    )
    return df

if __name__=="__main__":
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    plot_parser = subparsers.add_parser("plot")
    plot_parser.add_argument("--country", "-c", required=True)
    plot_parser.add_argument("--log", action="store_true")

    list_parser = subparsers.add_parser("list")
    args = parser.parse_args()

    gdp_df = gdp()
    ghg_df = ghg()

    df = pd.merge(
        gdp_df, ghg_df,
        left_on=["country", "year"],
        right_on=["country", "year"]
    )
    df = df.sort_values(["country", "year"])

    if args.command == "list":
        for c in df["country"].unique():
            print(c)
    else:
        # Make sure everything is sorted, and then normalize the values based on 1980 values
        df["gdp"] = df.groupby("country")["gdp"].transform(lambda x: x / x.iloc[0] * 100)
        df["ghg"] = df.groupby("country")["ghg"].transform(lambda x: x / x.iloc[0] * 100)
        
        one_country = df[df["country"] == args.country].sort_values("year")
        slope, _ = np.polyfit(np.log(one_country["gdp"]), np.log(one_country["ghg"]), 1)
        r2 = one_country[["gdp", "ghg"]].corr().iloc[0, 1] ** 2
        ax = one_country.plot(x="year", y=["gdp", "ghg"], logy=args.log)
        plt.legend(["GDP", "GHG"])
        ax.text(0.05, 0.95, f"Slope = {slope:.3f}", transform=ax.transAxes, va="top")
        plt.show()

