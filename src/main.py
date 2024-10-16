import numpy as np

class Recommender:
    def __init__(self, matrix_file, metric='cosine', neighbors=5, prediction_type='simple'):
      self.metric = metric
      self.neighbors = neighbors
      self.prediction_type = prediction_type
      self.load_matrix(matrix_file)

    def load_matrix(self, matrix_file):
      with open(matrix_file, 'r') as f:
        lines = f.readlines()
        self.min_rating = float(lines[0].strip())
        self.max_rating = float(lines[1].strip())
        ratings = [line.strip().split() for line in lines[2:]]
        
        # Replace "-" with NaN and convert to a NumPy array
        self.utility_matrix = np.array([
            [float(r) if r != '-' else np.nan for r in row]
            for row in ratings
        ])



# check if the class is working
matrix_file = "matrix.txt"
metric = "pearson"
neighbors = 5
prediction_type = "simple"
recommender = Recommender(matrix_file, metric=metric, neighbors=neighbors, prediction_type=prediction_type)


