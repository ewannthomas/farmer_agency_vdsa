import pandas as pd
from utils.dir_values import dir_values


"""This script calls on the GICC datsets created by the gicc_data_create.py file for creating output mentioned under the casual_enquiries.md file"""
"""Input files from: /frer/data/interim/stata_files"""
"""Output files to: ./frer/results"""

# defining directories
raw_path, interim_path, long_path, processed_path, external_path = dir_values()


def count_fem_hh_cop_mech():
    """How many female headed households adopted what coping mechanism for each calamity?"""
    stata_file_path = interim_path.joinpath("stata_files/gicc_fam_info_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        (df.groupby(["problem", "cop_mech"])["hh_id_panel"].nunique())
        .reset_index()
        .pivot(index=["cop_mech"], columns="problem", values="hh_id_panel")
        .reset_index()
    )
    result_file = results_folder.joinpath("count_fem_hh_cop_mech.csv")
    df.to_csv(result_file, index=False)


def count_fem_hh_inputs():
    """How many female headed households gave highest rank for assistances from institutions, during flood and drought?"""
    stata_file_path = interim_path.joinpath("stata_files/gicc_fam_info_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        (
            df[df["rank"] == 1].groupby(["institutions"])["hh_id_panel"].nunique()
        ).reset_index()
        # .pivot(index=["cop_mech"], columns="problem", values="hh_id_panel")
        # .reset_index()
    )
    result_file = results_folder.joinpath("count_fem_hh_inputs.csv")
    df.to_csv(result_file, index=False)


def count_fem_hh_cop_mech_yr():
    """How many female headed households adopted what coping mechanism in each year for each calamity?"""
    stata_file_path = interim_path.joinpath("stata_files/gicc_fam_info_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        (df.groupby(["sur_yr", "problem", "cop_mech"])["hh_id_panel"].nunique())
        .reset_index()
        .pivot(index=["sur_yr", "cop_mech"], columns="problem", values="hh_id_panel")
        .reset_index()
    )
    result_file = results_folder.joinpath("count_fem_hh_cop_mech_by_yr.csv")
    df.to_csv(result_file, index=False)


def count_fem_hh_info():
    """Count of unique households which sought advice for each activity from each institution"""

    stata_file_path = interim_path.joinpath("stata_files/gicc_fam_info_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        (df[df["rank"] == 1].groupby(["institutions"])["hh_id_panel"].nunique())
        .reset_index()
        .rename(columns={"hh_id_panel": "count of female hh"})
    )
    result_file = results_folder.joinpath("count_fem_hh_inputs.csv")
    df.to_csv(result_file, index=False)


def count_fem_hh_reliab_rank():
    """How many female headed households gave highest rank for assistances from institutions, during flood and drought?"""
    stata_file_path = interim_path.joinpath("stata_files/gicc_fam_reliab_rank.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        (
            df[df["reliab_rank"] == 1]
            .groupby(["calamity", "sou_assistance"])["hh_id_panel"]
            .nunique()
        )
        .reset_index()
        .rename(columns={"hh_id_panel": "count of female hh"})
    )

    df = df.pivot(
        index="sou_assistance",
        columns="calamity",
        values="count of female hh",
    ).reset_index()

    result_file = results_folder.joinpath("count_fem_hh_reliab_rank.csv")
    df.to_csv(result_file, index=False)


"""Does access to information and institutions by the household vary by caste of household head?"""


def count_caste_info():
    """Does access to information and institutions by the household vary by caste of household head?"""
    stata_file_path = interim_path.joinpath("stata_files/gen_info_ranking.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        df[df["rank"] == 1]
        .groupby(["caste_group", "institutions"])["hh_id_panel"]
        .nunique()
    ).reset_index()

    df = df.pivot(
        index="institutions",
        columns="caste_group",
        values="hh_id_panel",
    ).reset_index()

    result_file = results_folder.joinpath("count_caste_info.csv")
    df.to_csv(result_file, index=False)


def count_caste_info_yr():
    """Does access to information and institutions by the household vary by caste of household head?"""
    stata_file_path = interim_path.joinpath("stata_files/gen_info_ranking.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        df[df["rank"] == 1]
        .groupby(["sur_yr", "caste_group", "institutions"])["hh_id_panel"]
        .nunique()
    ).reset_index()

    df = df.pivot(
        index=["sur_yr", "institutions"],
        columns="caste_group",
        values="hh_id_panel",
    ).reset_index()

    result_file = results_folder.joinpath("count_caste_info_yr.csv")
    df.to_csv(result_file, index=False)


"""Does households belonging to different castes adopt different coping mechanisms?"""


def caste_cop_mech_all():
    """Does households belonging to different castes adopt different coping mechanisms?"""

    """All necessary levels are included. Lengthy table!"""
    stata_file_path = interim_path.joinpath("stata_files/caste_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        df.groupby(["caste_group", "problem", "adopted_by", "cop_mech"])[
            "hh_id_panel"
        ].nunique()
    ).reset_index()

    df = df.pivot(
        index=[
            "caste_group",
            "problem",
            "adopted_by",
        ],
        columns="cop_mech",
        values="hh_id_panel",
    ).reset_index()

    result_file = results_folder.joinpath("count_caste_cop_mech_all.csv")
    df.to_csv(result_file, index=False)


def caste_cop_mech():
    """Does households belonging to different castes adopt different coping mechanisms?"""

    """All necessary levels are included. Lengthy table!"""
    stata_file_path = interim_path.joinpath("stata_files/caste_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        df.groupby(["caste_group", "cop_mech"])["hh_id_panel"].nunique()
    ).reset_index()

    df = df.pivot(
        index=[
            "caste_group",
        ],
        columns="cop_mech",
        values="hh_id_panel",
    ).reset_index()

    result_file = results_folder.joinpath("count_caste_cop_mech.csv")
    df.to_csv(result_file, index=False)


def caste_cop_mech_problem():
    """Does households belonging to different castes adopt different coping mechanisms?"""

    """All necessary levels are included. Lengthy table!"""
    stata_file_path = interim_path.joinpath("stata_files/caste_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        df.groupby(["caste_group", "problem", "cop_mech"])["hh_id_panel"].nunique()
    ).reset_index()

    df = df.pivot(
        index=[
            "caste_group",
            "problem",
        ],
        columns="cop_mech",
        values="hh_id_panel",
    ).reset_index()

    result_file = results_folder.joinpath("count_caste_cop_mech_problem.csv")
    df.to_csv(result_file, index=False)


def caste_cop_mech_all_yr():
    """Does households belonging to different castes adopt different coping mechanisms?"""

    """All necessary levels are included. Lengthy table!"""
    stata_file_path = interim_path.joinpath("stata_files/caste_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        df.groupby(["sur_yr", "caste_group", "problem", "adopted_by", "cop_mech"])[
            "hh_id_panel"
        ].nunique()
    ).reset_index()

    df = df.pivot(
        index=[
            "sur_yr",
            "caste_group",
            "problem",
            "adopted_by",
        ],
        columns="cop_mech",
        values="hh_id_panel",
    ).reset_index()

    result_file = results_folder.joinpath("count_caste_cop_mech_all_yr.csv")
    df.to_csv(result_file, index=False)


def caste_cop_mech_yr():
    """Does households belonging to different castes adopt different coping mechanisms?"""

    """All necessary levels are included. Lengthy table!"""
    stata_file_path = interim_path.joinpath("stata_files/caste_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        df.groupby(["sur_yr", "caste_group", "cop_mech"])["hh_id_panel"].nunique()
    ).reset_index()

    df = df.pivot(
        index=[
            "sur_yr",
            "caste_group",
        ],
        columns="cop_mech",
        values="hh_id_panel",
    ).reset_index()

    result_file = results_folder.joinpath("count_caste_cop_mech_yr.csv")
    df.to_csv(result_file, index=False)


def caste_cop_mech_problem_yr():
    """Does households belonging to different castes adopt different coping mechanisms?"""

    """All necessary levels are included. Lengthy table!"""
    stata_file_path = interim_path.joinpath("stata_files/caste_cop_mech.csv")
    results_folder = raw_path.parents[1].joinpath("results/feedback")

    df = pd.read_csv(stata_file_path)

    df = (
        df.groupby(["sur_yr", "caste_group", "problem", "cop_mech"])[
            "hh_id_panel"
        ].nunique()
    ).reset_index()

    df = df.pivot(
        index=[
            "sur_yr",
            "caste_group",
            "problem",
        ],
        columns="cop_mech",
        values="hh_id_panel",
    ).reset_index()

    result_file = results_folder.joinpath("count_caste_cop_mech_problem_yr.csv")
    df.to_csv(result_file, index=False)


"""Does coping mechanism adopted by a household vary by the ownership status of land?"""
