# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:21:52 2020

@author: Mastermind
"""


import pandas as pd
pd.options.display.max_columns = 8


# =============================================================================
# TODO: Organise Into Modules
# =============================================================================
# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 142: Table I
# =============================================================================
period = (
    1879,
    1889,
    1899,
    1904,
    1909,
    1914,
    1919,
    1922,
)
bldg_per = (
    13.,
    13.4,
    14.8,
    15.8,
    16.,
    16.2,
    16.4,
    16.5,
)
mach_per = (
    24.,
    24.3,
    25.9,
    27.5,
    28.1,
    28.7,
    29.5,
    30.,
)
bldg_val = (
    363,
    879,
    1450,
    1996,
    2948,
    3692,
    7293,
    8681,
)
mach_val = (
    670,
    1584,
    2543,
    3490,
    5178,
    6541,
    13118,
    15783,
)

df = pd.DataFrame.from_dict(
    {
        'period': period,
        'bldg_per': bldg_per,
        'mach_per': mach_per,
        'bldg_val': bldg_val,
        'mach_val': mach_val,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df['val'] = df.iloc[:, 2].add(df.iloc[:, 3])
FILE_NAME = 'theory_of_production_table1.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 144
# =============================================================================
val = (
    200,
    210,
    216,
    184,
    148,
    141,
    211,
    282,
    241,
    263,
)
per = (
    9.6,
    10,
    10.3,
    8.8,
    7.1,
    6.7,
    10,
    13.5,
    11.5,
    12.5,
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1880 + _ for _ in range(10)),
        'val': val,
        'per': per,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df.loc['Total'] = df.sum()
FILE_NAME = 'theory_of_production_table1_.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 145: Table II
# =============================================================================
col_a = (
    339,
    264,
    277,
    342,
    328,
    282,
    457,
    612,
    629,
    373,
    569,
    422,
    379,
    457,
    497,
    356,
    1017,
    1899,
    2891,
    2473,
    1898,
    2096,
    780,
    1177,
)
col_b = (
    88,
    89,
    88,
    89,
    91,
    87,
    92,
    100,
    106,
    94,
    96,
    100,
    99,
    103,
    110,
    101,
    105,
    135,
    173,
    183,
    196,
    237,
    184,
    181,
)
col_c = (
    387,
    297,
    315,
    383,
    362,
    326,
    494,
    611,
    595,
    397,
    591,
    420,
    384,
    443,
    453,
    353,
    967,
    1402,
    1673,
    1350,
    969,
    884,
    424,
    650,
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1899 + _ for _ in range(24)),
        'col_a': col_a,
        'col_b': col_b,
        'col_c': col_c,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df['col_c'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100).round().astype(int)
df['col_d'] = df.iloc[:, 2].cumsum().add(4062)
df['col_e'] = df.iloc[:, 3].div(df.iloc[0, 3]).mul(100).round().astype(int)
FILE_NAME = 'theory_of_production_table2.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 146
# =============================================================================
ma = (
    105,
    110,
    113,
    130,
    130,
    150,
    188,
    210,
    248,
    250,
)
us = (
    104,
    110,
    116,
    120,
    132,
    154,
    188,
    217,
    239,
    263,
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1911 + _ for _ in range(10)),
        'ma': ma,
        'us': us,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
FILE_NAME = 'theory_of_production_table2_.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 148: Table III
# =============================================================================
lab = (
    4713,
    4968,
    5184,
    5554,
    5784,
    5468,
    5906,
    6251,
    6483,
    5714,
    6615,
    6807,
    6855,
    7167,
    7277,
    7026,
    7269,
    8601,
    9218,
    9446,
    9096,
    9110,
    6947,
    7602,
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1899 + _ for _ in range(24)),
        'lab': lab,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df['idx'] = df.iloc[:, 0].div(df.iloc[0, 0]).mul(100).round().astype(int)
FILE_NAME = 'theory_of_production_table3.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 149: Table IV
# =============================================================================
pro = (
    100,
    101,
    112,
    122,
    124,
    122,
    143,
    152,
    151,
    126,
    155,
    159,
    153,
    177,
    184,
    169,
    189,
    225,
    227,
    223,
    218,
    231,
    179,
    240,
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1899 + _ for _ in range(24)),
        'pro': pro,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
FILE_NAME = 'theory_of_production_table4.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 152: Table VI
# =============================================================================
pro_com = (
    101,
    107,
    112,
    121,
    126,
    123,
    133,
    141,
    148,
    137,
    155,
    160,
    163,
    170,
    174,
    171,
    179,
    209,
    227,
    236,
    233,
    236,
    194,
    209,
)
pro = (
    100,
    101,
    112,
    122,
    124,
    122,
    143,
    152,
    151,
    126,
    155,
    159,
    153,
    177,
    184,
    169,
    189,
    225,
    227,
    223,
    218,
    231,
    179,
    240,
)
dev = (
    -1,
    -6,
    0,
    0.8,
    -1.6,
    -0.8,
    7,
    7,
    2,
    -9,
    0,
    -0.6,
    -6.5,
    4,
    5.5,
    -1.2,
    5,
    7.2,
    0,
    -6,
    -7,
    -2.2,
    -8.4,
    13,
)
ba = (
    'Подъём',
    'Подъём; Кратковременный Рецессия',
    'Подъём',
    'Подъём',
    'Подъём; рецессия',
    'Умеренный спад; оживление',
    'Подъём',
    'Подъём',
    'Подъём, паника, рецессия, Спад',
    'Спад',
    'Оживление, умеренный подъём',
    'Рецессия',
    'Умеренный спад',
    'Оживление; подъём',
    'Подъём; рецессия',
    'Спад',
    'Оживление; подъём',
    'Подъём',
    'Подъём; военные действия',
    'Военные действия; рецессия',
    'Оживление; подъём',
    'Подъём; рецессия, спад',
    'Спад',
    'Оживление; подъём',
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1899 + _ for _ in range(24)),
        'pro_com': pro_com,
        'pro': pro,
        'dev': dev,
        'ba': ba,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df['abs'] = df.iloc[:, 2].abs()
print(f'{df.iloc[:, 4].mean():,.6f}')
FILE_NAME = 'theory_of_production_table6.dat'
# df.iloc[:, range(4)].to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 159: Table VIII
# =============================================================================
pro = (
    100,
    101,
    112,
    122,
    124,
    122,
    143,
    152,
    151,
    126,
    155,
    159,
    153,
    177,
    184,
    169,
    189,
    225,
    227,
    223,
    218,
    231,
    179,
    240,
)
pro_com = (
    101,
    106,
    111,
    119,
    125,
    123,
    133,
    142,
    149,
    139,
    157,
    163,
    166,
    173,
    178,
    176,
    185,
    214,
    234,
    244,
    243,
    247,
    208,
    223,
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1899 + _ for _ in range(24)),
        'pro': pro,
        'pro_com': pro_com,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df['dev'] = df.iloc[:, 0].sub(df.iloc[:, 1]).div(
    df.iloc[:, 0]).mul(100).round().astype(int)
FILE_NAME = 'theory_of_production_table8.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 161
# =============================================================================
idx = (
    100,
    96,
    102,
    103,
    101,
    105,
    114,
    115,
    110,
    104,
    110,
    110,
    105,
    116,
    119,
    113,
    123,
    123,
    116,
    111,
    113,
    119,
    121,
    149,
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1899 + _ for _ in range(24)),
        'idx': idx,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
FILE_NAME = 'theory_of_production_table8_.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 162: Table IX
# =============================================================================
def_mfg = (
    100,
    105,
    101,
    103,
    104,
    103,
    106,
    112,
    119,
    110,
    112,
    115,
    111,
    116,
    117,
    113,
    119,
    156,
    210,
    226,
    242,
    284,
    186,
    179,
)
def_all = (
    100,
    108,
    106,
    113,
    114,
    114,
    115,
    118,
    125,
    120,
    129,
    135,
    124,
    132,
    134,
    131,
    135,
    169,
    237,
    259,
    276,
    302,
    196,
    199,
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1899 + _ for _ in range(24)),
        'def_mfg': def_mfg,
        'def_all': def_all,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df['ratio'] = df.iloc[:, 0].mul(100).div(df.iloc[:, 1]).round().astype(int)
FILE_NAME = 'theory_of_production_table4.dat'
df_pro = pd.read_csv(FILE_NAME, sep='\t')
df_pro.set_index('period', inplace=True)
df['pro'] = df_pro.iloc[:, 0].mul(df.iloc[:, 2]).div(100).round().astype(int)
FILE_NAME = 'theory_of_production_table9.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 163: Table X
# =============================================================================
idx = (
    101,
    95,
    99,
    95,
    93,
    96,
    106,
    111,
    105,
    96,
    97,
    95,
    96,
    103,
    106,
    98,
    110,
    115,
    104,
    98,
    102,
    114,
    117,
    136,
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1899 + _ for _ in range(24)),
        'idx': idx,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
FILE_NAME = 'theory_of_production_table10.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 163: Footnote 37
# =============================================================================
period = (
    1909,
    1911,
    1913,
    1915,
    1917,
    1910,
    1912,
    1914,
    1916,
    1918,
)
value = (
    72.2,
    76.4,
    74.5,
    75.4,
    71.0,
    71.6,
    74.5,
    77.8,
    68.7,
    78.1,
)

df = pd.DataFrame.from_dict(
    {
        'period': period,
        'value': value,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df.sort_index(inplace=True)
print(f'{df.iloc[:, 0].mean():,.6f}')
df.plot(grid=True)


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page 164: Table XI
# =============================================================================
pro_val = (
    101,
    95,
    99,
    95,
    93,
    96,
    106,
    111,
    105,
    96,
    97,
    95,
    96,
    103,
    106,
    98,
    110,
    115,
    104,
    98,
    102,
    114,
    117,
    136,
)
wages = (
    99,
    98,
    101,
    102,
    100,
    99,
    103,
    101,
    99,
    94,
    102,
    104,
    97,
    99,
    100,
    99,
    99,
    104,
    103,
    107,
    111,
    114,
    115,
    119,
)
ba = (
    '',
    'Brief Recession',
    '',
    '',
    '',
    'Mild Depression',
    '',
    '',
    '',
    'Depression',
    '',
    '',
    'Mild Depression',
    '',
    '',
    'Depression',
    '',
    '',
    'War',
    'War',
    '',
    '',
    'Depression',
    '',
)

df = pd.DataFrame.from_dict(
    {
        'period': tuple(1899 + _ for _ in range(24)),
        'pro_val': pro_val,
        'wages': wages,
        'ba': ba,
    }
)
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df['dev'] = df.iloc[:, 1].sub(df.iloc[:, 0]).div(
    df.iloc[:, 0]).mul(100).round().astype(int)
df['pro_val_rm_7'] = df.iloc[:, 0].rolling(7).mean()
df['wages_rm_7'] = df.iloc[:, 1].rolling(7).mean()
df['dev_abs'] = df.iloc[:, -3].abs()
df.plot(grid=True)
print(f'{df.iloc[:, -1].mean():,.6f}')
print(df.corr())
print(df)
FILE_NAME = 'theory_of_production_table11.dat'
df.to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page ?: Table ?
# =============================================================================
FILE_NAME = 'theory_of_production_table2.dat'
df_a = pd.read_csv(FILE_NAME, sep='\t')
FILE_NAME = 'theory_of_production_table3.dat'
df_b = pd.read_csv(FILE_NAME, sep='\t')
df_a.set_index(df_a.columns[0], inplace=True)
df_b.set_index(df_b.columns[0], inplace=True)
df = pd.concat(
    [
        df_a.iloc[:, [4]],
        df_b.iloc[:, [1]],
    ],
    axis=1)
df['lab_to_cap'] = df.iloc[:, 1].div(
    df.iloc[:, 0]).mul(100).round().astype(int)
FILE_NAME = 'theory_of_production_table5.dat'
df.iloc[:, [2]].to_csv(FILE_NAME, sep='\t')


# =============================================================================
# Cobb C.W., Douglas P.H. A Theory of Production, 1928, Page ?: Table ?
# =============================================================================
FILE_NAME = 'theory_of_production_table6.dat'
df = pd.read_csv(FILE_NAME, sep='\t', usecols=range(3))
df.set_index(df.columns[0], inplace=True, verify_integrity=True)
df['sub_pro'] = df.iloc[:, 1].sub(
    df.iloc[:, 1].rolling(window=3, center=True).mean())
df['sub_pro_com'] = df.iloc[:, 0].sub(
    df.iloc[:, 0].rolling(window=3, center=True).mean())
df.dropna(inplace=True)
df = df.astype(int)
FILE_NAME = 'theory_of_production_table7.dat',
df.to_csv(FILE_NAME, sep='\t')
