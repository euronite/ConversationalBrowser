#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime
import itertools


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


def read_in_data():
    return pd.read_csv("../data/genderedCorpus.csv", sep=",", names=header_names)


def receiver_and_caller_column(df):
    """
    Takes in the dataframe, header names and gender/position.
    This then looks at person_and_type column and fills the caller and receiver column with the appropriate value
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


def get_conversation_topic_df(df, topic):
    """
    Gets the rows that match the conversation topic specified.
    """
    return df.loc[df["conversation_topic"] == topic]


def remove_conversation_topic_df(df, topic):
    """
    Gets the rows that do not contain a specific topic. Can pass a string containing topics to remove.
    Delimited by a comma
    """
    for individual_topic in topic.split(","):
        df = df.loc[df["conversation_topic"] != individual_topic]
    return df


def get_call_df(df, call_id):
    """
    This gets the rows containing the call_id.
    """
    return df.loc[df["call"] == call_id]


def get_all_call_ids(df):
    """
    Returns an array of the names of the call ids
    """
    return df.call.unique()


def get_all_conversation_topics(df):
    """
    Returns array of all the names of the conversation topics
    """
    return df.conversation_topic.unique()


def get_conversation_only_df(df, non_verbal_speech):
    """
    Return df with non-verbal speech removed
    """
    for cue in non_verbal_speech:
        df = df[~df["person_and_type"].str.contains(cue)]
    return df


def get_rows_by_caller_and_receiver(df, caller, receiver):
    """
    Specify the caller and receiver string and returns the dataframe with those rows.
    """
    return df.loc[(df["caller"] == caller) & (df["receiver"] == receiver)]


def convert_to_minutes_and_seconds(seconds):
    return datetime.timedelta(seconds=seconds)


def get_permutations_of_gender_and_position():
    """
    Takes in the gender_and_position var and returns the possible combinations of size 2
    """
    permutations = list(itertools.permutations(gender_and_position, 2))
    final_permutation = []
    for perm in permutations:
        if "caller" in perm[0]:
            if "receiver" in perm[1]:
                final_permutation.append(perm)
    return [" ".join(i) for i in final_permutation]


def occurrence_of_each_event(df, types):
    """
    This takes in a dataframe and produces the total number of each conversation cue occurred.
    """
    occurrences = df["person_and_type"].value_counts()
    for occurrence_name in occurrences.index:
        for cue_type in types:
            if occurrence_name.count(cue_type) > 1:
                types[cue_type] += occurrences[occurrence_name] * 2
            elif occurrence_name.count(cue_type) == 1:
                types[cue_type] += occurrences[occurrence_name]
    return types


def total_time_of_each_event(df, types):
    """
    This calculates the total time of each cue in the dataset, returning a dictionary of each cue
    """
    for cue in types:
        new_df = df[
            df["person_and_type"].str.contains(cue)
        ]  # for each cue, get df of all rows containing cue
        types[cue] = (new_df["end"] - new_df["start"]).sum(
            axis=0
        )  # end time - start time and sum them all
    return types


def mean_time_of_each_event(df, types):
    """
    Gets the mean of each conversation cue. Returns a dictionary.
    """
    for cue in types:
        new_df = df[df["person_and_type"].str.contains(cue)]
        if len(new_df) > 0:
            types[cue] = (new_df["end"] - new_df["start"]).mean(axis=0)
    return types


def mean_call_length(df):
    total = 0
    ids = get_all_call_ids(df)
    for call in ids:
        new_df = df[df["call"].str.match(call)]
        total += new_df.iloc[-1]["end"]
    return total / len(ids)


def individual_call_length(df):
    """
    Gets the the call length of each conversation and returns a dictionary of call id and length of time
    """
    total = {}
    ids = get_all_call_ids(df)
    for call in ids:
        temp_df = df[df["call"].str.match(call)]  # gets the df that matches call id
        total[call] = temp_df.iloc[-1]["end"]
    return total


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
