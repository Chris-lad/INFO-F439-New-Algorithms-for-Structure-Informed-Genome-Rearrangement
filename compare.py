import os
from scipy.stats import pearsonr, spearmanr


def compute_correlation():
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'output-with-q-count.txt')
    jaccardfile = os.path.join(dirname, 'jaccard_reversed_indexes.txt')
    xs = [[], [], []]
    ys = [[], [], []]
    with open(filename) as f, open(jaccardfile) as j:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            linejac = j.readline()
            if lines[i][0] == '-':
                _, cluster, q_count = lines[i].strip().split()
                q_count = int(q_count)
                n_orders = len(lines[i+1].split())
                linejac = j.readline()
                xs[q_count].extend([float(e) for e in lines[i+1].strip().split()])
                ys[q_count].extend([float(e) for e in linejac.strip().split()])
                is_correct = True
                i += n_orders
            i += 1
        for q_count in range(3):
            print()
            print("Number of Q-nodes =", q_count)
            print(pearsonr(xs[q_count], ys[q_count]))
            print(spearmanr(xs[q_count], ys[q_count]))
            print()


def compare_paper():
    dirname = os.path.dirname(__file__)
    filename1 = os.path.join(dirname, 'output.txt')
    filename2 = os.path.join(dirname, 'paper-output.txt')
    with open(filename1) as f1, open(filename2) as f2:
        correct_clusters = 0
        lines = f1.readlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            line2 = f2.readline()
            if len(line.split()) == 1:
                cluster = line.strip()
                n_orders = len(lines[i+1].split())
                is_correct = True
                for j in range(n_orders):
                    i += 1
                    line = lines[i]
                    line2 = f2.readline()
                    output = [float(x) for x in line.strip().split()]
                    paper_output = [float(x) for x in line2.strip().split()]
                    if output != paper_output:
                        is_correct = False
                if is_correct:
                    correct_clusters += 1
                else:
                    print(cluster)
            i += 1
        print(correct_clusters)


if __name__ == '__main__':
    compute_correlation()