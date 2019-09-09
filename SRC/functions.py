import argparse
from clean import df_ff, df_ff_state_pop_income
from analysis import state_conclusion
import seaborn as sns
sns.set(color_codes=True)


def get_args(argv=None):
    valid_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
                    'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Palau', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    valid_foodtypes = ['mexican', 'sandwich', 'italian', 'chicken', 'fish', 'asian',
                       'burger', 'ice cream', 'mediterranean', 'middle east', 'hot dog', 'american fast food']
    parser = argparse.ArgumentParser(
        description="Get USA state and fast food company name")
    parser.add_argument("--state", "-s", type=str,
                        choices=valid_states, help="USA State name")
    parser.add_argument("--fastfoodtype", "-f", type=str, choices=valid_foodtypes,
                        help="fast food type")
    return parser.parse_args(argv)


def avg_income(state):
    return "Average household income in {} -> ${}".format(state, int(df_ff_state_pop_income[df_ff_state_pop_income.state == state]['avg_income']))


def ranking_avg_income(state):
    df_state_income = df_ff_state_pop_income.sort_values(
        by=['avg_income'], ascending=False).reset_index(drop=True)
    return "{} is the state nº {} in average income".format(state, df_state_income[df_state_income.state == state].index[0] + 1)


def ranking_ff_rest(state):
    df_state_ff_rest = df_ff_state_pop_income.sort_values(
        by=['ffrest_percapita'], ascending=False).reset_index(drop=True)
    return "{} is the state nº {} in number of fast food restaurants per capita(10K)".format(state, df_state_ff_rest[df_state_ff_rest.state == state].index[0] + 1)


def ranking_ff_type(state, fastfoodtype):
    df_state_ff_type = df_ff[df_ff.categories == fastfoodtype].groupby(
        ['state'], as_index=False).count()
    df_state_ff_type.sort_values(
        by=['categories'], ascending=False).reset_index(drop=True)
    if len(df_state_ff_type[df_state_ff_type.state == state]) > 0:
        ranking = df_state_ff_type[df_state_ff_type.state ==
                                   state].index[0] + 1
        # mejorar esto!!!!!!!!!!!!!!!
        if ranking > 3:
            ranking = "{}th ".format(ranking)
        if ranking == 1:
            ranking = ""
        if ranking == 2:
            ranking = "second "
        if ranking == 3:
            ranking = "third "
        return "{} is the {}state with more {} restaurants in the US".format(state, ranking, fastfoodtype)
    return "{} has no {} restaurants (disclaimer: analysis done with a subset of the whole dataset - not available for free)".format(state, fastfoodtype)


def report_generator(state, fastfoodtype):
    return "{}\n{}\n{}\n{}\n{}".format(ranking_avg_income(state), ranking_ff_rest(state), state_conclusion, ranking_ff_type(state, fastfoodtype), avg_income(state))


def plot_generator(state, df=df_ff_state_pop_income):
    df['my_state'] = df['state'].apply(
        lambda text: state if text == state else "Rest of States")
    plot = sns.lmplot(x="avg_income", y="ffrest_percapita", hue="my_state", legend="full", fit_reg=False,
                      data=df, palette="Paired")
    sns.regplot(x="avg_income", y="ffrest_percapita",
                data=df, scatter=False, ax=plot.axes[0, 0])
    return plot.set_axis_labels("Avg household income ($)", "# fast food restaurants (per 10K people)")
