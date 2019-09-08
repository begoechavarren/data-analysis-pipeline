import argparse
from clean import df_ff, df_ff_state_pop_income


def get_args(argv=None):
    valid_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
                    'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Palau', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    parser = argparse.ArgumentParser(
        description="Get USA state and fast food company name")
    parser.add_argument("--state", "-s", type=str,
                        choices=valid_states, help="USA State name")
    parser.add_argument("--fastfoodcompany", "-f", type=str,
                        help="USA fast food company")
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


def ranking_ff_company(state, fastfoodcompany):
    df_state_ff_company = df_ff[df_ff.name == fastfoodcompany].groupby(
        ['state'], as_index=False).count()
    df_state_ff_company.sort_values(
        by=['name'], ascending=False).reset_index(drop=True)
    ranking = df_state_ff_company[df_state_ff_company.state ==
                                  state].index[0] + 1
    num = len(df_ff[(df_ff.name == fastfoodcompany)
                    & (df_ff.state == state)].index)
    return "{} is the state nº {} in number of {}s with {} restaurants".format(state, ranking, fastfoodcompany, num)


def report_generator(state, fastfoodcompany):
    return "{}\n{}\n{}\n{}".format(ranking_avg_income(state), ranking_ff_rest(state), ranking_ff_company(state, fastfoodcompany), avg_income(state))
