from functions import *

path = "data/regression"
sample_size = (224, 224)
num_samples = 500

initDirectory(path)
createSamplesAndMetrics(path, sample_size, num_samples, (1,20), (3,20))