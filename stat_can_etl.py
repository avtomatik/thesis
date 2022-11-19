# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:20:54 2021

@author: Alexander Mikhailov
"""


import os
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from read.lib import read_can
from toolkit.lib import build_push_data_frame, string_to_url

# =============================================================================
# Capital
# # 16100077-eng.xlsx: NO;
# # 16100088-eng.xlsx: NO;
# # 16100118-eng.xlsx: NO;
# # 34100278-eng.xlsx: NO;
# # 34100279-eng.xlsx: NO;
# # 36100096-eng.xlsx: YES;
# # 36100097-eng.xlsx: NO;
# # 36100109-eng.xlsx: NO;
# # 36100174-eng.xlsx: NO;
# # 36100210-eng.xlsx: NO;
# # 36100236-eng.xlsx: YES ALTERNATIVE;
# # 36100237-eng.xlsx: YES ALTERNATIVE;
# # 36100238-eng.xlsx: NO;
# =============================================================================
# =============================================================================
# Labor
# # 14100027-eng.xlsx: YES;
# # 14100036-eng.xlsx: NO;
# # 14100221-eng.xlsx: NO;
# # 14100235-eng.xlsx: YES;
# # 14100238-eng.xlsx: NO;
# # 14100242-eng.xlsx: NO;
# # 14100243-eng.xlsx: NO;
# # 14100259-eng.xlsx: MAYBE;
# # 14100265-eng.xlsx: YES;
# # 14100355-eng.xlsx: MAYBE;
# # 14100392-eng.xlsx: NO;
# # 36100489-eng.xlsx: NO;
# =============================================================================
# =============================================================================
# Production
# # 10100094-eng.xlsx: Capacity utilization rates (Bank of Canada calculated series), seasonally adjusted
# # 16100013-eng.xlsx: NO;
# # 16100038-eng.xlsx: NO;
# # 16100047-eng.xlsx: NO;
# # 16100052-eng.xlsx: NO;
# # 16100053-eng.xlsx: NO;
# # 16100054-eng.xlsx: NO;
# # 16100056-eng.xlsx: NO;
# # 16100079-eng.xlsx: NO;
# # 16100109-eng.xlsx: Industrial capacity utilization rates, by industry
# # 16100111-eng.xlsx: Industrial capacity utilization rates, by Standard Industrial Classification, 1980 (SIC)
# # 16100117-eng.xlsx: NO;
# # 16100119-eng.xlsx: NO;
# # 36100207-eng.xlsx: NO;
# # 36100208-eng.xlsx: Capital stock: v41713073;
# # 36100217-eng.xlsx: NO;
# # 36100303-eng.xlsx: NO;
# # 36100305-eng.xlsx: NO;
# # 36100309-eng.xlsx: NO;
# # 36100310-eng.xlsx: NO;
# # 36100383-eng.xlsx: NO;
# # 36100384-eng.xlsx: NO;
# # 36100385-eng.xlsx: YES;
# # 36100386-eng.xlsx: YES;
# # 36100480-eng.xlsx: Total number of jobs: v111382232;
# # 36100488-eng.xlsx: Output, by sector and industry, provincial and territorial: v64602050;
# =============================================================================


def build_push_data_frame(file_name: str, blueprint: dict) -> None:
    """
    Builds DataFrame & Loads It To Excel

    Parameters
    ----------
    file_name : str
        Excel File Name.
    blueprint : dict
        DESCRIPTION.

    Returns
    -------
    None
    """
    df = DataFrame()
    for item in blueprint:
        _df = read_can(
            string_to_url(item['archive_name']),
            index_col=0,
            usecols=range(14),
            parse_dates=True
        )
        _df = _df[_df['VECTOR'].isin(item['series_ids'])]
        for series_id in item['series_ids']:
            chunk = _df[_df['VECTOR'] == series_id][['VALUE']]
            chunk = chunk.groupby(chunk.index.year).mean()
            df = pd.concat([df, chunk], axis=1, sort=True)
        df.columns = item['series_ids']
    # df.to_excel(archive_name)


CAPITAL = (
    {
        'archive_name': '36100096-eng.zip',
        'series_ids':
        (
            'v90968617', 'v90968618', 'v90968619', 'v90968620', 'v90968621',
            'v90971177', 'v90971178', 'v90971179', 'v90971180', 'v90971181',
            'v90973737', 'v90973738', 'v90973739', 'v90973740', 'v90973741',
        ),
    },
    {
        'archive_name': '36100210-eng.zip',
        'series_ids':
        (
            'v46444563', 'v46444624', 'v46444685', 'v46444746', 'v46444807',
            'v46444929', 'v46444990', 'v46445051', 'v46445112', 'v46445173',
            'v46445295', 'v46445356', 'v46445417', 'v46445478', 'v46445539',
            'v46445661', 'v46445722', 'v46445783', 'v46445844', 'v46445905',
        ),
    },
    {
        'archive_name': '36100236-eng.zip',
        'series_ids':
        (
            'v1071434', 'v1071435', 'v1071436', 'v1071437', 'v64498363',
            'v1119722', 'v1119723', 'v1119724', 'v1119725', 'v64498371',
            'v4421025', 'v4421026', 'v4421027', 'v4421028', 'v64498379',
        ),
    },
)
LABOUR = (
    {
        'archive_name': '14100027-eng.zip',
        'series_ids':
        ('v2523013', ),
    },
    {
        'archive_name': '14100221-eng.zip',
        'series_ids':
        ('v54027148', 'v54027152', ),
    },
    {
        'archive_name': '14100235-eng.zip',
        'series_ids':
        ('v74989', ),
    },
    {
        'archive_name': '14100238-eng.zip',
        'series_ids':
        ('v1596771', ),
    },
    {
        'archive_name': '14100243-eng.zip',
        'series_ids':
        ('v78931172', 'v78931174', 'v78931173', ),
    },
    {
        'archive_name': '14100265-eng.zip',
        'series_ids':
        ('v249139', 'v249703', 'v250265', ),
    },
    {
        'archive_name': '14100355-eng.zip',
        'series_ids':
        ('v2057609', 'v123355112', 'v2057818', ),
    },
    {
        'archive_name': '14100392-eng.zip',
        'series_ids':
        ('v1235071986', ),
    },
    {
        'archive_name': '36100489-eng.zip',
        'series_ids':
        (
            'v65521825',
            # =================================================================
            # # =================================================================
            # # Not Useful
            # # =================================================================
            # 'v65522120',
            # # =================================================================
            # # Not Useful
            # # =================================================================
            # 'v65522415',
            # =================================================================
        ),
    },
)
PRODUCT = (
    {
        'archive_name': '10100094-eng.zip',
        'series_ids':
            ('v37482', ),
    },
    {
        'archive_name': '16100053-eng.zip',
        'series_ids':
            ('v535579', 'v535593', 'v535663', 'v535677', ),
    },
    {
        'archive_name': '16100054-eng.zip',
        'series_ids':
            ('v761808', 'v761927', ),
    },
    {
        'archive_name': '16100109-eng.zip',
        'series_ids':
            ('v4331088', ),
    },
    {
        'archive_name': '16100111-eng.zip',
        'series_ids':
            ('v142817', ),
    },
    {
        'archive_name': '36100207-eng.zip',
        'series_ids':
            ('v21573668', 'v21573686', ),
    },
    {
        'archive_name': '36100208-eng.zip',
        'series_ids':
            (
                # =============================================================
                # # =============================================================
                # # Not Useful: Labour input
                # # =============================================================
                # 'v41712954',
                # =============================================================
                'v41713056', 'v41713073', 'v41713243',
            ),
    },
    {
        'archive_name': '36100217-eng.zip',
        'series_ids':
            ('v86718697', 'v86719219', ),
    },
    {
        'archive_name': '36100303-eng.zip',
        'series_ids':
            ('v716397', 'v718173', ),
    },
    {
        'archive_name': '36100305-eng.zip',
        'series_ids':
            ('v719421', ),
    },
    {
        'archive_name': '36100309-eng.zip',
        'series_ids':
            (
                'v41707475',
                # =============================================================
                # # =============================================================
                # # Not Useful: Labour input
                # # =============================================================
                # 'v41707595',
                # =============================================================
                'v41707775', 'v41708195', 'v41708375', ),
    },
    {
        'archive_name': '36100310-eng.zip',
        'series_ids':
            (
                'v42189127',
                # =============================================================
                # # =============================================================
                # # Not Useful: Labour input
                # # =============================================================
                # 'v42189231',
                # =============================================================
                'v42189387', 'v42189751', 'v42189907',
            ),
    },
    {
        'archive_name': '36100386-eng.zip',
        'series_ids':
            ('v11567', ),
    },
    {
        'archive_name': '36100480-eng.zip',
        'series_ids':
            ('v111382232', ),
    },
    {
        'archive_name': '36100488-eng.zip',
        'series_ids':
            ('v64602050', ),
    },
)


def main():
    DIR = '/home/green-machine/data_science/data/interim'
    os.chdir(DIR)
    FILE_NAME = 'stat_can_desc.xlsx'
    FILE_NAMES = (
        'stat_can_cap.xlsx',
        'stat_can_lab.xlsx',
        'stat_can_prd.xlsx',
    )
    _FILE_NAME = 'stat_can_desc.xlsx'

    # =========================================================================
    # Construct Excel File from Specification
    # =========================================================================
    for file_name, blueprint in zip(FILE_NAMES, (CAPITAL, LABOUR, PRODUCT)):
        build_push_data_frame(file_name, blueprint)

    # =============================================================================
    # # =============================================================================
    # # Retrieve Series Description
    # # =============================================================================
    # _df = pd.concat(
    #     [
    #         pd.read_excel(Path(DIR).joinpath(file_name), index_col=0)
    #         for file_name in FILE_NAMES
    #     ],
    #     axis=1
    # )
    #
    # desc = pd.merge(
    #     pd.read_excel(Path(DIR).joinpath(FILE_NAME), index_col=0),
    #     _df.transpose(),
    #     left_index=True,
    #     right_index=True,
    # )
    # desc.transpose().to_excel(Path(DIR).joinpath(_FILE_NAME))
    # =============================================================================


if __name__ == '__main__':
    main()
