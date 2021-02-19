#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This holds the actual data manipulation functions for the conversational data browser. They will be called when needed.
"""

import pandas as pd
from itertools import permutations as iterpermutations

header_names = [
    "call",
    "conversation_topic",
    "person_and_type",
    "start",
    "end",
    "caller",
    "receiver",
]
gender_and_position = {"caller_F", "receiver_F", "caller_M", "receiver_M"}
gender_types = dict.fromkeys(gender_and_position, 0)
cue_types = {"laughter": 0, "silence": 0, "filler": 0, "bc": 0}


def read_in_data(location):
    return pd.read_csv(location, sep=",", names=header_names)


def receiver_and_caller_column(df):
    """
    Takes in the dataframe, header names and gender/position.
    This then looks at person_and_type column and fills the caller and receiver column with the appropriate value
    :return: df data frame containing the data set with additional caller and receiver columns
    """
    call_id = get_all_call_ids(df)
    for call in call_id:
        temp_df = get_call_df(df, call)  # get dataframe of only one call id
        for gp in gender_and_position:
            if temp_df["person_and_type"].str.contains(gp).any():
                if "receiver" in gp:
                    df.loc[df.call == call, "receiver"] = gp
                else:
                    df.loc[df.call == call, "caller"] = gp
    return df


def get_call_df(df, call_id: str):
    """
    This gets the rows containing a specific caller ID.
    :param df: dataset that is being searched
    :param call_id: str the caller ID that is being located
    :return: df of rows with caller id.
    """
    return df.loc[df["call"] == call_id]


def get_all_call_ids(df):
    """
    Returns an array of the names of the call ids
    :param: df dataframe of the dataset being searched
    :return: array of call IDs.
    """
    return df.call.unique()


def get_list_of_call_id_df(df, call_id_list: list):
    """
    This finds the rows where the call ID matches one of the call ids being searched for.
    :param df: dataset that is being searched
    :param call_id_list: a list of call ids that are being matched.
    :return: df of rows where the call id is in the call_id list
    """
    return df[(df.call.isin(call_id_list))]


def get_non_verbal_speech_only(df, non_verbal_speech: str):
    """
    Return df with non-verbal speech cue rows only.
    :param df: dataset
    :param non_verbal_speech: str containing the cue being searched
    :return: df with only the rows that contain said cue.
    """
    df = df[df["person_and_type"].str.contains(non_verbal_speech)]
    return df


def get_rows_by_caller_and_receiver(df, caller: str, receiver: str):
    """
    Specify the caller and receiver string and returns the dataframe with those rows by searching the receiver and
    caller columns.
    :param df: dataset
    :param caller: str of caller in the format caller_<M/F>
    :param receiver: str of receiver in the format receiver_<M/F>
    :return: df containing the caller and receiver specified.
    """
    if receiver is not None and caller is None:
        return df.loc[(df["receiver"] == receiver)]
    elif caller is not None and receiver is None:
        return df.loc[(df["caller"] == caller)]
    elif caller is not None and receiver is not None:
        return df.loc[(df["caller"] == caller) & (df["receiver"] == receiver)]
    else:
        return df


def get_permutations_of_gender_and_position() -> list:
    """
    Takes in the gender_and_position var and returns the possible combinations of size 2
    :return: list of gender and positions as caller/receiver.
    """
    permutations = list(iterpermutations(gender_and_position, 2))
    final_permutation = []
    for perm in permutations:
        if "caller" in perm[0]:
            if "receiver" in perm[1]:
                final_permutation.append(perm)
    return [" ".join(i) for i in final_permutation]


def occurrence_of_each_event(df, types: dict) -> dict:
    """
    This takes in a dataframe and produces the total number of each conversation cue occurred.
    :param df: dataset
    :param types: dict of types is the cue being searched for.
    :return: types: dict of types along with their frequency.
    """
    occurrences = df["person_and_type"].value_counts()
    for occurrence_name in occurrences.index:
        for cue_type in types:
            if occurrence_name.count(cue_type) > 1:
                types[cue_type] += occurrences[occurrence_name] * 2
            elif occurrence_name.count(cue_type) == 1:
                types[cue_type] += occurrences[occurrence_name]
    return types


def get_all_event_durations(df, cue: str) -> list:
    """
    This gets the duration of a single cue and returns it as a list of the caller and receiver
    :param df: dataset
    :param cue: the cue that is being searched
    :return: list of caller and receiver durations.
    """
    if df.empty:
        raise ValueError("Dataframe is empty")
    if "M" in df["receiver"].iloc[0]:
        receiver_search = f"{cue}_rM"
    else:
        receiver_search = f"{cue}_rF"
    if "M" in df["caller"].iloc[0]:
        caller_search = f"{cue}_cM"
    else:
        caller_search = f"{cue}_cF"
    if cue == "silence":
        receiver_search = "silence"
        caller_search = "silence"
    receiver_df = get_non_verbal_speech_only(df, receiver_search)
    receiver_df = receiver_df["end"] - receiver_df["start"]
    caller_df = get_non_verbal_speech_only(df, caller_search)
    caller_df = caller_df["end"] - caller_df["start"]
    return [caller_df, receiver_df]


def occurrence_of_event(df, cue: str) -> list:
    """
    returns a list of two vals. number of times caller did a cue and number of times the receiver did the cue
    :param df: datset of an individual call.
    :param cue: str cue that is being searched
    :return: list of the cue count, caller and receiver.
    """
    if df.empty:
        raise ValueError("Dataframe is empty")
    if "M" in df["receiver"].iloc[0]:
        receiver_search = f"{cue}_rM"
    else:
        receiver_search = f"{cue}_rF"
    if "M" in df["caller"].iloc[0]:
        caller_search = f"{cue}_cM"
    else:
        caller_search = f"{cue}_cF"
    if cue == "silence":
        receiver_search = "silence"
        caller_search = "silence"
    caller_cue_count = df.person_and_type.str.count(caller_search).sum()
    receiver_cue_count = df.person_and_type.str.count(receiver_search).sum()
    return [caller_cue_count, receiver_cue_count]


def total_time_of_event(df, cue: str) -> list:
    """
    This calculates the total duration of a single cue, for a single call.
    :param df: this is a dataframe containing the rows of a single call ID.
    :param cue: cue that is being used.
    :return: [caller_cue_time, receiver_cue_time] a list of the duration of the cue chosen.
    """
    if df.empty:
        raise ValueError("Dataframe empty")
    if "M" in df["receiver"].iloc[0]:
        receiver_search = f"{cue}_rM"
    else:
        receiver_search = f"{cue}_rF"
    if "M" in df["caller"].iloc[0]:
        caller_search = f"{cue}_cM"
    else:
        caller_search = f"{cue}_cF"
    caller_cue_time = df[df["person_and_type"].str.contains(caller_search)]
    caller_cue_time = (caller_cue_time["end"] - caller_cue_time["start"]).sum(axis=0)
    receiver_cue_time = df[df["person_and_type"].str.contains(receiver_search)]
    receiver_cue_time = (receiver_cue_time["end"] - receiver_cue_time["start"]).sum(
        axis=0
    )
    return [caller_cue_time, receiver_cue_time]


def total_time_of_each_event(df, types: dict) -> dict:
    """
    This calculates the total time of each cue from the types dict in the dataset, returning a dictionary of each cue.
    :param df: contains the dataset.
    :param types: dict of the cues being searched for
    :return: types: dict of the cue durations.
    """
    for cue in types:
        new_df = df[
            df["person_and_type"].str.contains(cue)
        ]  # for each cue, get df of all rows containing cue
        types[cue] = (new_df["end"] - new_df["start"]).sum(
            axis=0
        )  # end time - start time and sum them all
    return types


def mean_time_of_each_event(df, types: dict) -> dict:
    """
    Gets the mean of each conversation cue. Returns the cue average time.
    :param df: dataset being searched
    :param types: dict of the cues being searched and the duration at 0
    :return: dict of average cue durations.
    """
    for cue in types:
        new_df = df[df["person_and_type"].str.contains(cue)]
        if len(new_df) > 0:
            types[cue] = (new_df["end"] - new_df["start"]).mean(axis=0)
    return types


def total_overlap_occurrence(df):
    """
    Returns the number of times there was two people talking over on another
    """
    permutations = get_permutations_of_gender_and_position()
    return df[df["person_and_type"].isin(permutations)].shape[0]


def total_overlap_time(df):
    permutations = get_permutations_of_gender_and_position()
    new_df = df[df["person_and_type"].isin(permutations)]
    total = (new_df["end"] - new_df["start"]).sum(
        axis=0
    )  # end time - start time and sum them all
    return total


def mean_overlap_time(df):
    """
    Calculates the overlap mean time.
    """
    permutations = get_permutations_of_gender_and_position()
    new_df = df[df["person_and_type"].isin(permutations)]
    return (new_df["end"] - new_df["start"]).mean(axis=0)
