import pandas as pd
import os


cases_filepath = r'data_access/cases.csv'
voivodeships_filepath = r'data_access/voivodeships.csv'
updates_filepath = r'data_access/update.csv'


def get_voivodeships() -> pd.DataFrame:
    return pd.read_csv(voivodeships_filepath)


def get_cases() -> pd.DataFrame:
    return pd.read_csv(cases_filepath)


def get_updates() -> pd.DataFrame:
    return pd.read_csv(updates_filepath)


def save_update(update) -> None:
    update.to_csv(updates_filepath, index=False, header=False, mode='a')


def get_cases_filtered(voivodeship: str = None, date_from: str = None, date_to: str = None) -> pd.DataFrame:
    cases = get_cases()
    if len(cases) > 0:
        cases = cases.groupby(by=['voivodeship', 'date'], as_index=False).sum()
    if voivodeship is not None:
        cases = cases[cases.voivodeship == voivodeship]
    if date_from is not None:
        cases = cases[cases.date >= date_from]
    if date_to is not None:
        cases = cases[cases.date <= date_to]
    cases.sort_values(by='date', inplace=True)
    cases.reset_index(inplace=True)
    return cases


def get_cases_grouped(voivodeship: str = None, date_from: str = None, date_to: str = None) -> pd.DataFrame:
    cases = get_cases_filtered(voivodeship, date_from, date_to)
    cases = cases.groupby('voivodeship').sum()
    cases.reset_index(inplace=True)
    return cases


def save_new_cases(new_cases: pd.DataFrame) -> None:
    if not os.path.isfile(cases_filepath):
        new_cases.to_csv(cases_filepath, index=False)
    else:
        cases = pd.read_csv(cases_filepath)
        date = new_cases['date'].unique()[0]
        daily_cases = cases[cases.date == date]
        if len(daily_cases) == 0:
            new_cases.to_csv(cases_filepath, index=False, header=False, mode='a')
        else:
            if date <= '2020-06-10':
                is_not_duplicate = False
                for voivodeship in new_cases.voivodeship.values:
                    saved_cases = daily_cases[daily_cases.voivodeship == voivodeship]
                    new_cases_to_save = new_cases[new_cases.voivodeship == voivodeship]
                    if saved_cases.cases.values[0] != new_cases_to_save.cases.values[0]:
                        is_not_duplicate = True
                if is_not_duplicate:
                    new_cases.to_csv(cases_filepath, index=False, header=False, mode='a')

