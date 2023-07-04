import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info
from utils.coping_mech import cop_mech

interim_path, long_path, results_folder = dir_values()

"""Does coping mechanism adopted by a household vary by the features of land owned?"""

"""Number of tables: """


def land():
    tag = "Landholding"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)
    return df


def merger():
    df_left = land()
    df_right = cop_mech()

    df = pd.merge(
        left=df_left,
        right=df_right,
        on=["hh_id", "sur_yr", "hh_id_panel"],
        how="outer",
        validate="m:m",
        indicator=True,
    )

    df = merger_info(df)

    return df


# Feature 1 : Soil Type
def count_hh_soil_type():
    """Number of households by soild type of land owned"""
    stats_file = results_folder.joinpath("count_hh_soil_type.csv")
    if not stats_file.exists():
        df = merger()

        df = df.groupby(["soil_type"])["hh_id_panel"].nunique().reset_index()

        df.to_csv(stats_file, index=False)


def count_hh_soil_type_yr():
    """Number of households by soil type of land owned and year"""
    stats_file = results_folder.joinpath("count_hh_soil_type_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = df.groupby(["sur_yr", "soil_type"])["hh_id_panel"].nunique().reset_index()

        df = df.pivot(
            index="sur_yr", columns="soil_type", values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)


def count_soil_type_cop_mech():
    """Number of households by soild type of land owned"""
    stats_file = results_folder.joinpath("count_soil_type_cop_mech.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["soil_type", "cop_mech"])["hh_id_panel"].nunique().reset_index()
        )

        df = df.pivot(
            index="soil_type", columns="cop_mech", values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)


def count_soil_type_cop_mech_yr():
    """Number of households by soil type of land owned and year"""
    stats_file = results_folder.joinpath("count_soil_type_cop_mech_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["sur_yr", "soil_type", "cop_mech"])["hh_id_panel"]
            .nunique()
            .reset_index()
        )

        df = df.pivot(
            index=["sur_yr", "soil_type"], columns="cop_mech", values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)


# Feature 2 : Ownership status of land
def count_hh_own_status():
    """Number of households by ownership status of land"""
    stats_file = results_folder.joinpath("count_hh_own_status.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["onwership_status_landholding"])["hh_id_panel"]
            .nunique()
            .reset_index()
        )

        df.to_csv(stats_file, index=False)


def count_hh_own_status_yr():
    """Number of households by ownership status of land and year"""
    stats_file = results_folder.joinpath("count_hh_own_status_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["sur_yr", "onwership_status_landholding"])["hh_id_panel"]
            .nunique()
            .reset_index()
        )

        df = df.pivot(
            index="sur_yr", columns="onwership_status_landholding", values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)


def count_own_status_cop_mech():
    """Number of households by ownership status of land and coping mechansim adopted"""
    stats_file = results_folder.joinpath("count_own_status_cop_mech.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["onwership_status_landholding", "cop_mech"])["hh_id_panel"]
            .nunique()
            .reset_index()
        )
        df = df.pivot(
            index=["cop_mech"],
            columns="onwership_status_landholding",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)


def count_own_status_cop_mech_yr():
    """Number of households by year, ownership status of land and coping mechansim adopted"""
    stats_file = results_folder.joinpath("count_own_status_cop_mech_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["sur_yr", "onwership_status_landholding", "cop_mech"])[
                "hh_id_panel"
            ]
            .nunique()
            .reset_index()
        )

        df = df.pivot(
            index=["sur_yr", "onwership_status_landholding"],
            columns="cop_mech",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)


# Feature 3: Source of Irrigation
def count_hh_irri_source():
    """Number of households by source of irrigation (sou_irri_1) of land owned"""
    stats_file = results_folder.joinpath("count_hh_irri_source.csv")
    if not stats_file.exists():
        df = merger()

        df = df.groupby(["sou_irri_1"])["hh_id_panel"].nunique().reset_index()

        df.to_csv(stats_file, index=False)


def count_hh_irri_source_yr():
    """Number of households by source of irrigation of land owned and year"""
    stats_file = results_folder.joinpath("count_hh_irri_source_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = df.groupby(["sur_yr", "sou_irri_1"])["hh_id_panel"].nunique().reset_index()

        df = df.pivot(
            index="sur_yr", columns="sou_irri_1", values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)


def count_irri_source_cop_mech():
    """Number of households by source of irrigation of land owned and coping mechanism"""
    stats_file = results_folder.joinpath("count_irri_source_cop_mech.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["sou_irri_1", "cop_mech"])["hh_id_panel"]
            .nunique()
            .reset_index()
        )

        df = df.pivot(
            index="sou_irri_1", columns="cop_mech", values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)


def count_irri_source_cop_mech_yr():
    """Number of households by year, source of irrigation of land owned and coping mechanism"""
    stats_file = results_folder.joinpath("count_irri_source_cop_mech_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["sur_yr", "sou_irri_1", "cop_mech"])["hh_id_panel"]
            .nunique()
            .reset_index()
        )

        df = df.pivot(
            index=["sur_yr", "cop_mech"], columns="sou_irri_1", values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)
