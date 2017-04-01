#!/usr/bin/python

algorithms = ["bf","ff","wf"]

#tuple (cpu, mem)
recurso_serv = [("5.0", "9.6"), ("2.5", "4.8"),
                ("1.0", "1.9")]

recurso_req = ["normal", "grande"]

num_repeticoes = 5

with open("experiment_inputs.txt", "w") as txt:
  for alg in algorithms:
    for r_serv in recurso_serv:
      for r_req in recurso_req:
        for i in range(num_repeticoes):
          txt.write(','.join([alg, r_serv[0], r_serv[1],
                              r_req]) + "\n")
