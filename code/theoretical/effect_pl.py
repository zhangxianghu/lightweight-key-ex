from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as pt
import pandas as pd


# Test number of test keys----------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------


# test case 1.1: pc = 0.05, pf = 0.01, t = 4
# pt.rcParams.update({'font.size': 12})
# pt.figure(figsize=[5, 4])
# pt.subplots_adjust(left=0.15, right=0.98, top=0.88, bottom=0.15)

# X1 = [0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]
# Y1 = [14,14,14,14,14,14,14]
# Y2 = [13,13,13,13,13,13,13]
# Y3 = [13,13,13,13,13,13,13]
# Y4 = [12,12,12,12,12,12,12]

# host = host_subplot(111)

# host.set_xlabel("Packet loss rate $p_l$", fontsize=14)
# host.set_ylabel("Number of test keys $N_t$", fontsize=14)

# host.set_ylim(5, 65)   #y range
# host.plot(X1,Y1, 'b',marker='.', label="Number of helper parties n = 6")
# host.scatter(X1,Y1,marker='.', color="b")

# host.plot(X1,Y2, 'y',marker='^', label="Number of helper parties n = 8")
# host.scatter(X1,Y2,marker='^', color="y")

# host.plot(X1,Y3, 'r',marker='s', label="Number of helper parties n = 10")
# host.scatter(X1,Y3,marker='s', color="r")

# host.plot(X1,Y4, 'g',marker='*', label="Number of helper parties n = 12")
# host.scatter(X1,Y4,marker='*', color="g")

# leg = pt.legend(loc="upper left", prop={'size': 9})
# pt.setp(leg.get_texts(),fontsize=14)

# pt.title('$p_f = 0.01, p_c = 0.05$')
# pt.savefig('../figures/effect_pl_pc005_k.pdf')

# pt.show()

# # --------------------------------

# # test case 2.1: pc = 0.10, pf = 0.01, t = 4
# pt.rcParams.update({'font.size': 12})
# pt.figure(figsize=[5, 4])
# pt.subplots_adjust(left=0.15, right=0.98, top=0.88, bottom=0.15)

# X1 = [0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]
# Y1 = [24, 24, 24, 24, 24, 24, 24]
# Y2 = [22, 22, 22, 22, 22, 22, 22]
# Y3 = [21, 21, 21, 21, 21, 21, 21]
# Y4 = [20, 20, 20, 20, 20, 20, 20]

# host = host_subplot(111)

# host.set_xlabel("Packet loss rate $p_l$", fontsize=14)
# host.set_ylabel("Number of test keys $N_t$", fontsize=14)

# host.set_ylim(5, 65)   #y range
# host.plot(X1,Y1, 'b',marker='.', label="Number of helper parties n = 6")
# host.scatter(X1,Y1,marker='.', color="b")

# host.plot(X1,Y2, 'y',marker='^', label="Number of helper parties n = 8")
# host.scatter(X1,Y2,marker='^', color="y")

# host.plot(X1,Y3, 'r',marker='s', label="Number of helper parties n = 10")
# host.scatter(X1,Y3,marker='s', color="r")

# host.plot(X1,Y4, 'g',marker='*', label="Number of helper parties n = 12")
# host.scatter(X1,Y4,marker='*', color="g")


# pt.title('$p_f = 0.01, p_c = 0.10$')
# pt.savefig('../figures/effect_pl_pc010_k.pdf')

# pt.show()

# # --------------------------------

# # test case 3.1: pc = 0.15, pf = 0.01, t = 4
# pt.rcParams.update({'font.size': 12})
# pt.figure(figsize=[5, 4])
# pt.subplots_adjust(left=0.15, right=0.98, top=0.88, bottom=0.15)

# X1 = [0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]
# Y1 = [39, 39, 39, 39, 39, 39, 39]
# Y2 = [33, 33, 33, 33, 33, 33, 33]
# Y3 = [31, 31, 31, 31, 31, 31, 31]
# Y4 = [30, 30, 30, 30, 30, 30, 30]

# host = host_subplot(111)

# host.set_xlabel("Packet loss rate $p_l$", fontsize=14)
# host.set_ylabel("Number of test keys $N_t$", fontsize=14)

# host.set_ylim(5, 65)   #y range
# host.plot(X1,Y1, 'b',marker='.', label="Number of helper parties n = 6")
# host.scatter(X1,Y1,marker='.', color="b")

# host.plot(X1,Y2, 'y',marker='^', label="Number of helper parties n = 8")
# host.scatter(X1,Y2,marker='^', color="y")

# host.plot(X1,Y3, 'r',marker='s', label="Number of helper parties n = 10")
# host.scatter(X1,Y3,marker='s', color="r")

# host.plot(X1,Y4, 'g',marker='*', label="Number of helper parties n = 12")
# host.scatter(X1,Y4,marker='*', color="g")


# pt.title('$p_f = 0.01, p_c = 0.15$')
# pt.savefig('../figures/effect_pl_pc015_k.pdf')

# pt.show()

# # --------------------------------

# # test case 4.1: pc = 0.20, pf = 0.01, t = 4
# pt.rcParams.update({'font.size': 12})
# pt.figure(figsize=[5, 4])
# pt.subplots_adjust(left=0.15, right=0.98, top=0.88, bottom=0.15)

# X1 = [0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]
# Y1 = [63,63,63,63,63,63,63]
# Y2 = [51,51,51,51,51,51,51]
# Y3 = [46,46,46,46,46,46,46]
# Y4 = [43,43,43,43,43,43,43]

# host = host_subplot(111)

# host.set_xlabel("Packet loss rate $p_l$", fontsize=14)
# host.set_ylabel("Number of test keys $N_t$", fontsize=14)

# host.set_ylim(5, 65)   #y range
# host.plot(X1,Y1, 'b',marker='.', label="Number of helper parties n = 6")
# host.scatter(X1,Y1,marker='.', color="b")

# host.plot(X1,Y2, 'y',marker='^', label="Number of helper parties n = 8")
# host.scatter(X1,Y2,marker='^', color="y")

# host.plot(X1,Y3, 'r',marker='s', label="Number of helper parties n = 10")
# host.scatter(X1,Y3,marker='s', color="r")

# host.plot(X1,Y4, 'g',marker='*', label="Number of helper parties n = 12")
# host.scatter(X1,Y4,marker='*', color="g")


# pt.title('$p_f = 0.01, p_c = 0.20$')
# pt.savefig('../figures/effect_pl_pc020_k.pdf')

# pt.show()


# Test number of messages----------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------


# test case 4.2: pc = 0.20, pf = 0.01, t = 4
pt.rcParams.update({'font.size': 12})
pt.figure(figsize=[5, 4])
pt.subplots_adjust(left=0.15, right=0.98, top=0.88, bottom=0.15)

X1 = [0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]
Y1 = [567, 567, 567, 567, 567, 567, 567]
Y2 = [612, 612, 612, 612, 612, 612, 1224]
Y3 = [690, 690, 690, 690, 690, 690, 690]
Y4 = [774, 774, 774, 774, 774, 774, 774]

host = host_subplot(111)
# host = pt.subplots(figsize=(6,3.87))

host.set_xlabel("Packet loss rate $p_l$", fontsize=14)
host.set_ylabel("Number of messages $N_m$", fontsize=14)

host.set_ylim(100, 800)   #y range
host.plot(X1,Y1, 'b',marker='.', label="Number of helper parties n = 6")
host.scatter(X1,Y1,marker='.', color="b")

host.plot(X1,Y2, 'y',marker='^', label="Number of helper parties n = 8")
host.scatter(X1,Y2,marker='^', color="y")

host.plot(X1,Y3, 'r',marker='s', label="Number of helper parties n = 10")
host.scatter(X1,Y3,marker='s', color="r")

host.plot(X1,Y4, 'g',marker='*', label="Number of helper parties n = 12")
host.scatter(X1,Y4,marker='*', color="g")

pt.title('$p_f = 0.01, p_c = 0.20$')
pt.savefig('../figures/effect_pl_pc020_m.pdf')
pt.show()

# test case 3.2: pc = 0.15, pf = 0.01, t = 4
pt.rcParams.update({'font.size': 12})
pt.figure(figsize=[5, 4])
pt.subplots_adjust(left=0.15, right=0.98, top=0.88, bottom=0.15)
X1 = [0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]
Y1 = [351, 351, 351, 351, 351, 351, 702]
Y2 = [396, 396, 396, 396, 396, 396, 792]
Y3 = [465, 465, 465, 465, 465, 465, 465]
Y4 = [540, 540, 540, 540, 540, 540, 540]

host = host_subplot(111)

host.set_xlabel("Packet loss rate $p_l$", fontsize=14)
host.set_ylabel("Number of messages $N_m$", fontsize=14)

host.set_ylim(100, 800)   #y range
host.plot(X1,Y1, 'b',marker='.', label="Number of helper parties n = 6")
host.scatter(X1,Y1,marker='.', color="b")

host.plot(X1,Y2, 'y',marker='^', label="Number of helper parties n = 8")
host.scatter(X1,Y2,marker='^', color="y")

host.plot(X1,Y3, 'r',marker='s', label="Number of helper parties n = 10")
host.scatter(X1,Y3,marker='s', color="r")

host.plot(X1,Y4, 'g',marker='*', label="Number of helper parties n = 12")
host.scatter(X1,Y4,marker='*', color="g")

pt.title('$p_f = 0.01, p_c = 0.15$')
pt.savefig('../figures/effect_pl_pc015_m.pdf')
pt.show()

# leg = pt.legend(loc="lower left", prop={'size': 9})
# pt.setp(leg.get_texts(),fontsize=14)

# test case 2.2: pc = 0.10, pf = 0.01, t = 4
pt.rcParams.update({'font.size': 12})
pt.figure(figsize=[5, 4])
pt.subplots_adjust(left=0.15, right=0.98, top=0.88, bottom=0.15)
X1 = [0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]
Y1 = [216, 216, 216, 216, 216, 432, 432]
Y2 = [264, 264, 264, 264, 264, 264, 428]
Y3 = [315, 315, 315, 315, 315, 315, 315]
Y4 = [360, 360, 360, 360, 360, 360, 360]

host = host_subplot(111)

host.set_xlabel("Packet loss rate $p_l$", fontsize=14)
host.set_ylabel("Number of messages $N_m$", fontsize=14)

host.set_ylim(100, 800)   #y range
host.plot(X1,Y1, 'b',marker='.', label="Number of helper parties n = 6")
host.scatter(X1,Y1,marker='.', color="b")

host.plot(X1,Y2, 'y',marker='^', label="Number of helper parties n = 8")
host.scatter(X1,Y2,marker='^', color="y")

host.plot(X1,Y3, 'r',marker='s', label="Number of helper parties n = 10")
host.scatter(X1,Y3,marker='s', color="r")

host.plot(X1,Y4, 'g',marker='*', label="Number of helper parties n = 12")
host.scatter(X1,Y4,marker='*', color="g")

pt.title('$p_f = 0.01, p_c = 0.10$')
pt.savefig('../figures/effect_pl_pc010_m.pdf')
pt.show()

# # test case 1.2: pc = 0.05, pf = 0.01, t = 4
pt.rcParams.update({'font.size': 12})
pt.figure(figsize=[5, 4])
pt.subplots_adjust(left=0.15, right=0.98, top=0.88, bottom=0.15)
X1 = [0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]
Y1 = [126,126,126,126,126,252,252]
Y2 = [156,156,156,156,156,156,312]
Y3 = [195,195,195,195,195,195,195]
Y4 = [216,216,216,216,216,216,216]

host = host_subplot(111)

host.set_xlabel("Packet loss rate $p_l$", fontsize=14)
host.set_ylabel("Number of messages $N_m$", fontsize=14)

host.set_ylim(100, 800)   #y range
host.plot(X1,Y1, 'b',marker='.', label="Number of helper parties n = 6")
host.scatter(X1,Y1,marker='.', color="b")

host.plot(X1,Y2, 'y',marker='^', label="Number of helper parties n = 8")
host.scatter(X1,Y2,marker='^', color="y")

host.plot(X1,Y3, 'r',marker='s', label="Number of helper parties n = 10")
host.scatter(X1,Y3,marker='s', color="r")

host.plot(X1,Y4, 'g',marker='*', label="Number of helper parties n = 12")
host.scatter(X1,Y4,marker='*', color="g")

leg = pt.legend(loc="upper left", prop={'size': 9})
pt.setp(leg.get_texts(),fontsize=14)

pt.title('$p_f = 0.01, p_c = 0.05$')
pt.savefig('../figures/effect_pl_pc005_m.pdf')

pt.show()

