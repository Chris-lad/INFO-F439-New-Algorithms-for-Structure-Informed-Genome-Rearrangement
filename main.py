from PQtree import PQtree, Node, NodeType
from SignedString import SignedString
from Graph import Graph
import math
import os


def print_matrix(A: dict, nodes):
    n = len(list(A.values())[0])
    print(end='\t')
    for l in range(n):
        print(l, end='\t')
    print()
    for x in A.keys():
        print(x.char, end='\t')
        for l in range(n):
            print(A[x][l], end='\t')
        print()


def leaf_divergence(A, x, S2, d_Q_flip):
    l = S2.chars.find(x.char)
    x.l = l
    if x.sign == S2.signs[l]:
        A[x][l] = 0.0
    else:
        A[x][l] = d_Q_flip


def get_min_l_children(node):
    l = math.inf
    for child in node.children:
        if child.l is not None and child.l < l:
            l = child.l
    return l


def children_dist(A, node):
    dist = 0
    for x in node.children:
        dist += A[x][x.l]
    return dist


def is_flipped(x, x_prime):
    if x.sign == '*' or x_prime.sign == '*':
        flipped = False
    else:
        flipped = x.sign != x_prime.sign
    for i in range(len(x.children)):
        if x.children[i].char != x_prime.children[len(x.children)-i-1].char or \
            x.children[i].sign == x_prime.children[len(x.children)-i-1].sign:
            flipped = False
    return flipped


def flip_correction(x, equivalent, d_Q_flip):
    if not is_flipped(x, equivalent[x]):
        return 0
    correction = 0
    for child in x.children:
        if child.type == NodeType.Q_NODE or child.type == NodeType.LEAF:
            if is_flipped(child, equivalent[child]):
                correction += d_Q_flip
    return correction

def is_consecutive(j, k):
    return abs(j - k) == 1

def is_same_order(j, k):
    return k == j+1

def is_same_sign(s1, i, s2, j, k):
    return (s1.get_sign(i) == s2.get_sign(j) or s1.get_sign(i) == '*' or s2.get_sign(j) == '*') and \
        (s1.get_sign(i+1) == s2.get_sign(k) or s1.get_sign(i+1) == '*' or s2.get_sign(k) == '*')

def is_opposite_order(j, k):
    return k == j-1

def is_opposite_sign(s1, i, s2, j, k):
    return (s1.get_sign(i) != s2.get_sign(j) or s1.get_sign(i) == '*' or s2.get_sign(j) == '*') and \
        (s1.get_sign(i+1) != s2.get_sign(k) or s1.get_sign(i+1) == '*' or s2.get_sign(k) == '*')


def d_SBP(x, x_prime):
    s1 = x.substring()
    s2 = x_prime.substring()
    num_signed_breakpoint = 0
    for i in range(len(s1)-1):
        char1 = s1[i]
        char2 = s1[i+1]
        j = s2.index(char1)
        k = s2.index(char2)
        
        if is_consecutive(j, k) and \
            (is_same_order(j, k) and is_same_sign(s1, i, s2, j, k)) or \
            (is_opposite_order(j, k) and is_opposite_sign(s1, i, s2, j, k)):
            pass
        else:
            num_signed_breakpoint += 1
    # print(x, x_prime, num_signed_breakpoint)
    return num_signed_breakpoint

def delta_Q_violation(x, equivalent, d_Q_flip, d_Q_ord):
    return d_Q_ord * d_SBP(x, equivalent[x]) + is_flipped(x, equivalent[x]) * d_Q_flip

def delta_P_jump(x, equivalent):
    g = Graph()
    for child in x.children:
        g.add_node(child)
    for i in range(len(x.children)-1):
        y = x.children[i]
        k = equivalent[x].children.index(equivalent[y])
        for j in range(i+1, len(x.children)):
            z = x.children[j]
            t = equivalent[x].children.index(equivalent[z])
            if t < k:
                g.add_edge(y, z)
    weight, vertex_cover = g.get_minimum_vertex_cover_weight()
    return weight

def delta_P_violation(x, equivalent):
    return d_SBP(x, equivalent[x]) + delta_P_jump(x, equivalent)

def p_node_divergence(A, x, S2, equivalent):
    x.l = get_min_l_children(x)
    A[x][x.l] = children_dist(A, x) + delta_P_violation(x, equivalent)


def q_node_divergence(A, x, equivalent, d_Q_flip, d_Q_ord):
    x.l = get_min_l_children(x)
    e = 2 + len(x.children) - 1
    x.r = e

    A[x][x.l] = children_dist(A, x) + delta_Q_violation(x, equivalent, d_Q_flip, d_Q_ord) - flip_correction(x, equivalent, d_Q_flip)


def initialize_matrix(n, nodes):
    A = {}
    for x in nodes:
        A[x] = [math.inf for l in range(n)]
    return A


def measure_divergence(T, S1, T_prime, S2, d_Q_flip=0.5, d_Q_ord=1.5):
    n = len(S1)
    nodes = T.post_order()
    nodes_prime = T_prime.post_order()
    equivalent = {}
    for x in nodes:
        for x_prime in nodes_prime:
            if x.char == x_prime.char:
                equivalent[x] = x_prime
                equivalent[x_prime] = x

    A = initialize_matrix(n, nodes)
    for x in nodes:
        if x.type is NodeType.LEAF:
            leaf_divergence(A, x, S2, d_Q_flip)

        elif x.type is NodeType.P_NODE:
            p_node_divergence(A, x, S2, equivalent)

        else:
            q_node_divergence(A, x, equivalent, d_Q_flip, d_Q_ord)

    # print_matrix(A, nodes)
    return A[nodes[-1]][0]


def main_algo(trees):
    once = True
    for t1 in trees:
        for t2 in trees:
            T = PQtree.from_parenthesis_representation(t1)
            T_prime = PQtree.from_parenthesis_representation(t2)

            PQtree.add_equivalent_colors(T, T_prime)
            # print(T.post_order())
            # print(T_prime.post_order())
            if once:
                print(T.get_Q_node_count())
                once = False

            S1 = T.frontier()
            S2 = T_prime.frontier()

            m = measure_divergence(T, S1, T_prime, S2)
            
            T_prime.flip()
            S2 = T_prime.frontier()

            m_flipped = measure_divergence(T, S1, T_prime, S2)

            best_m = min(m, m_flipped)
            print(best_m, end=' ')
            # print()
            # print()
        print()

def main():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'pq-trees.txt')
    with open(filename) as f:
        name = None
        trees = []
        for line in f:
            if line[0] not in ['(', '[']:
                if name is not None:
                    print('-', name, end=' ')
                    main_algo(trees)
                name = line.strip()
                trees = []
            else:
                trees.append(line.strip())


if __name__ == '__main__':
    main()