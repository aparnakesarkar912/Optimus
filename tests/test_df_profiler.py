from pyspark.sql.types import *
from optimus import optimus as Optimus
from optimus.helpers.json import json_enconding
from optimus.helpers.functions import deep_sort
import unittest
from pyspark.ml.linalg import Vectors, VectorUDT, DenseVector
import numpy as np
nan = np.nan
import datetime
from pyspark.sql import functions as F
from optimus.profiler.profiler import Profiler
null = None
true = True
p= Profiler()
op = Optimus(master='local')
source_df=op.create.df([('names', StringType(), True),('height(ft)', ShortType(), True),('function', StringType(), True),('rank', ByteType(), True),('age', IntegerType(), True),('weight(t)', FloatType(), True),('japanese name', ArrayType(StringType(),True), True),('last position seen', StringType(), True),('date arrival', StringType(), True),('last date seen', StringType(), True),('attributes', ArrayType(FloatType(),True), True),('Date Type', DateType(), True),('timestamp', TimestampType(), True),('Cybertronian', BooleanType(), True),('function(binary)', BinaryType(), True),('NullType', NullType(), True)], [('Optimus', -28, 'Leader', 10, 5000000, 4.300000190734863, ['Inochi', 'Convoy'], '19.442735,-99.201111', '1980/04/10', '2016/09/10', [8.53439998626709, 4300.0], datetime.date(2016, 9, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Leader'), None), ('bumbl#ebéé  ', 17, 'Espionage', 7, 5000000, 2.0, ['Bumble', 'Goldback'], '10.642707,-71.612534', '1980/04/10', '2015/08/10', [5.334000110626221, 2000.0], datetime.date(2015, 8, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Espionage'), None), ('ironhide&', 26, 'Security', 7, 5000000, 4.0, ['Roadbuster'], '37.789563,-122.400356', '1980/04/10', '2014/07/10', [7.924799919128418, 4000.0], datetime.date(2014, 6, 24), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Security'), None), ('Jazz', 13, 'First Lieutenant', 8, 5000000, 1.7999999523162842, ['Meister'], '33.670666,-117.841553', '1980/04/10', '2013/06/10', [3.962399959564209, 1800.0], datetime.date(2013, 6, 24), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'First Lieutenant'), None), ('Megatron', None, 'None', 10, 5000000, 5.699999809265137, ['Megatron'], None, '1980/04/10', '2012/05/10', [None, 5700.0], datetime.date(2012, 5, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'None'), None), ('Metroplex_)^$', 300, 'Battle Station', 8, 5000000, None, ['Metroflex'], None, '1980/04/10', '2011/04/10', [91.44000244140625, None], datetime.date(2011, 4, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Battle Station'), None), (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)])
class Test_df_profiler(unittest.TestCase):
	maxDiff = None
	@staticmethod
	def test_columns_agg():
		actual_df =p.columns_agg(source_df,'*')
		actual_df =json_enconding(actual_df)
		expected_value =json_enconding({'names': {'count_uniques': 5, 'min': 'Jazz', 'max': 'ironhide&', 'count_na': 1, 'stddev': None, 'kurtosis': None, 'mean': None, 'skewness': None, 'sum': None, 'variance': None, 'zeros': 0}, 'height(ft)': {'count_uniques': 5, 'min': -28, 'max': 300, 'count_na': 2, 'stddev': 132.66612, 'kurtosis': 0.13863, 'mean': 65.6, 'skewness': 1.4049, 'sum': 328, 'variance': 17600.3, 'zeros': 0, 'percentile': {'0.75': 26, '0.95': 300, '0.05': -28, '0.25': 13, '0.5': 17}, 'hist': [{'count': 4.0, 'lower': -28.0, 'upper': 54.0}, {'count': 0.0, 'lower': 54.0, 'upper': 136.0}, {'count': 0.0, 'lower': 136.0, 'upper': 218.0}, {'count': 0.0, 'lower': 218.0, 'upper': 300.0}]}, 'function': {'count_uniques': 6, 'min': 'Battle Station', 'max': 'Security', 'count_na': 1, 'stddev': None, 'kurtosis': None, 'mean': None, 'skewness': None, 'sum': None, 'variance': None, 'zeros': 0}, 'rank': {'count_uniques': 3, 'min': 7, 'max': 10, 'count_na': 1, 'stddev': 1.36626, 'kurtosis': -1.5, 'mean': 8.33333, 'skewness': 0.3818, 'sum': 50, 'variance': 1.86667, 'zeros': 0, 'percentile': {'0.75': 10, '0.95': 10, '0.05': 7, '0.25': 7, '0.5': 8}, 'hist': [{'count': 4.0, 'lower': 7.0, 'upper': 8.5}, {'count': 0.0, 'lower': 8.5, 'upper': 10.0}]}, 'age': {'count_uniques': 1, 'min': 5000000, 'max': 5000000, 'count_na': 1, 'stddev': 0.0, 'kurtosis': nan, 'mean': 5000000.0, 'skewness': nan, 'sum': 30000000, 'variance': 0.0, 'zeros': 0, 'percentile': {'0.75': 5000000, '0.95': 5000000, '0.05': 5000000, '0.25': 5000000, '0.5': 5000000}, 'hist': [{'count': 6, 'lower': 5000000, 'upper': 5000001}]}, 'weight(t)': {'count_uniques': 5, 'min': 1.8, 'max': 5.7, 'count_na': 2, 'stddev': 1.64712, 'kurtosis': -1.43641, 'mean': 3.56, 'skewness': 0.06521, 'sum': 17.8, 'variance': 2.713, 'zeros': 0, 'percentile': {'0.75': 4.300000190734863, '0.95': 5.699999809265137, '0.05': 1.7999999523162842, '0.25': 2.0, '0.5': 4.0}, 'hist': [{'count': 1.0, 'lower': 1.8, 'upper': 2.78}, {'count': 0.0, 'lower': 2.78, 'upper': 3.75}, {'count': 2.0, 'lower': 3.75, 'upper': 4.73}, {'count': 1.0, 'lower': 4.73, 'upper': 5.7}]}, 'japanese name': {'count_uniques': 6, 'min': ['Bumble', 'Goldback'], 'max': ['Roadbuster'], 'count_na': 1}, 'last position seen': {'count_uniques': 4, 'min': '10.642707,-71.612534', 'max': '37.789563,-122.400356', 'count_na': 3, 'stddev': None, 'kurtosis': None, 'mean': None, 'skewness': None, 'sum': None, 'variance': None, 'zeros': 0}, 'date arrival': {'count_uniques': 1, 'min': '1980/04/10', 'max': '1980/04/10', 'count_na': 1, 'stddev': None, 'kurtosis': None, 'mean': None, 'skewness': None, 'sum': None, 'variance': None, 'zeros': 0}, 'last date seen': {'count_uniques': 6, 'min': '2011/04/10', 'max': '2016/09/10', 'count_na': 1, 'stddev': None, 'kurtosis': None, 'mean': None, 'skewness': None, 'sum': None, 'variance': None, 'zeros': 0}, 'attributes': {'count_uniques': 6, 'min': [None, 5700.0], 'max': [91.44000244140625, None], 'count_na': 1}, 'Date Type': {'count_uniques': 6, 'min': datetime.date(2011, 4, 10), 'max': datetime.date(2016, 9, 10), 'count_na': 1}, 'timestamp': {'count_uniques': 1, 'min': datetime.datetime(2014, 6, 24, 0, 0), 'max': datetime.datetime(2014, 6, 24, 0, 0), 'count_na': 1}, 'Cybertronian': {'count_uniques': 1, 'min': 1, 'max': 1, 'count_na': 1}, 'function(binary)': {'count_uniques': 6, 'min': bytearray(b'Battle Station'), 'max': bytearray(b'Security'), 'count_na': 1}, 'NullType': {'count_uniques': 0, 'min': None, 'max': None, 'count_na': 7}, 'p_count_na': 100.0, 'p_count_uniques': 0.0, 'range': 3.9000000000000004, 'median': 4.0, 'interquartile_range': 2.3000001907348633, 'coef_variation': 0.46267, 'mad': 1.7})
		assert(expected_value == actual_df)
