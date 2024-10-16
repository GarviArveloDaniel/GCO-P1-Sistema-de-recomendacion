def pearson (i, j):
  valid_i = [element for element in i if element != "-"]
  valid_j = [element for element in j if element != "-"]

  media_i = sum(valid_i) / len(valid_i)
  media_j = sum(valid_j) / len(valid_j)

  numerator = 0
  first_denom = 0
  second_denom = 0

  for element_i, element_j in zip(i,j):
    if (element_i != "-" and element_j != "-"):
      numerator += (element_i - media_i) * (element_j - media_j)
      first_denom += (element_i - media_i) ** 2
      second_denom += (element_j - media_j) ** 2
  
  return (numerator / ((first_denom ** 0.5) * (second_denom ** 0.5)))