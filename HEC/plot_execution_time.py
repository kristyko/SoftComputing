import matplotlib.pyplot as plt

RESULTS = "./results.txt"

n_processes = []
times = []
with open(RESULTS, "r") as file:
    experiments = file.readlines()
    for experiment in experiments:
        n, time = experiment.strip("\n").split()
        n_processes.append(int(n.strip("n:")))
        times.append(float(time.strip("time:")))

fig = plt.figure()
plt.plot(n_processes, times)
plt.xlabel("# processes")
plt.ylabel("execution time")
fig.savefig("./results_plot.png")
