import pytest
from app.mpt import *


#data = load_data(COINS)

#def test_crypto_list():
#
#    # Check each coin has at least half the days available
#    for c in data:
#        assert(len(data[c]) > 365)

DAY = 86400000

test_data = {
    "coin1":
        [
            [100 * DAY, 1],
            [200 * DAY, 1],
            [300 * DAY, 2]
            ],
    "coin2":
        [
            [100 * DAY, 1],
            [250 * DAY, 1],
            [300 * DAY, 2]
            ],
    "coin3":
        [
            [100 * DAY, 1],
            [200 * DAY, 2],
            [300 * DAY, 3]
            ]
    }


test_timestamp_data = {
        100 * DAY: {
            "coin1": 1,
            "coin2": 1,
            "coin3": 1
            },
        200 * DAY: {
            "coin1": 1,
            "coin3": 2
            },
        250 * DAY: {
            "coin2": 1
            },
        300 * DAY: {
            "coin1": 2,
            "coin2": 2,
            "coin3": 3
            }
    }


def test_transform_to_timestamp():



    timestamp_data = transform_to_timestamp(test_data)

    assert(timestamp_data[100 * DAY] == test_timestamp_data[100 * DAY])
    assert(timestamp_data[300 * DAY] == test_timestamp_data[300 * DAY])
    assert(timestamp_data[250 * DAY] == test_timestamp_data[250 * DAY])


def test_transform_to_dataframe():

    dataframe = transform_to_dataframe(test_timestamp_data)

    date = datetime.datetime.fromtimestamp(100 * DAY/1000).date()
    assert(dataframe.coin1.sum() == 4)
    assert(dataframe.coin2.sum() == 4)
    assert(dataframe.coin3.sum() == 6)

def test_clean_dataframe():

    dataframe = transform_to_dataframe(test_timestamp_data)
    dataframe = clean_dataframe(dataframe)
    assert(dataframe.coin1.sum() == 5)
    assert(dataframe.coin2.sum() == 5)
    assert(dataframe.coin3.sum() == 8)
    




