from tkinter import *

root = Tk()
root.geometry('900x556')  # Golden ratio
root.title('EEG Raw Data')

graphing_area = Canvas(root, width=900, height=556)
graphing_area.pack()

file = open('data.out', 'r')
lines = file.readlines()


def draw_point(points):
    average_point = 10

    i = 0
    graph_point = 0
    for point in points:
        if i % average_point == 0:
            graph_point += int((int(point)/99000)*556)
            graphing_area.create_rectangle(int(i), int(graph_point/(-1*average_point))+556,
                                           int(i), int(graph_point/(-1*average_point))+556)
            graph_point = 0
        else:
            graph_point += int((int(point)/99000)*556)
        i += 1


# stuff = []
# for line in lines:
#     if int(line[:-1]) > 99000: pass
#     else:
#         stuff.append(line[:-1])
#         print(line[:-1])
#
# ye = []
#
# for i in range(900):
#     ye.append(stuff[i])
#
# draw_point(ye)

root.mainloop()