# Copyright (c) 2016-2017, 15-021 Kim Shinyeop.
# This file is licensed under a Creative Commons license: CC BY-NC-SA.

ver = '3.0.0'
version = (3, 0, 0)

import random, csv

def myCmp(x, y):
    return cmp(x[0], y[0])

def readCsv(filename):
    matrix = []
    f = open(filename, 'r')
    csvReader = csv.reader(f)
    for row in csvReader:
        matrix.append(row)
    f.close()
    n = len(matrix)
    if filename == 'team.csv':
        for i in xrange(n):
            matrix[i][0] = int(matrix[i][0])
            matrix[i][3] = int(matrix[i][3])
        matrix.sort(myCmp)
    elif filename == 'data.csv':
        for i in xrange(n):
            matrix[i][0] = int(matrix[i][0])
            matrix[i][1] = int(matrix[i][1])
        matrix.sort(myCmp)
    return matrix

def convert(roomsM, roomsF):
    rooms = []
    for room in roomsM:
        rooms.append('A' + str(room))
    for room in roomsF:
        rooms.append('B' + str(room))
    rooms.sort()
    return rooms

def arrangeTickets(rooms, tno, tickets):
    r = len(rooms)
    t = len(tno)
    ticketsList = [[0]*t for i in xrange(r)]
    for ticket in tickets:
        try:
            j = rooms.index(ticket[2])
            k = tno.index(ticket[1])
            ticketsList[j][k] += 1
        except:
            pass
    return ticketsList

def countTickets(ticketsList):
    ticketsNum = []
    for ticketList in ticketsList:
        ticketsNum.append(sum(ticketList))
    return ticketsNum

def indexMax(nums):
    index = [0]
    maximum = nums[0]
    for i in xrange(len(nums)):
        if nums[i] > maximum:
            maximum = nums[i]
            index = [i]
        elif nums[i] == maximum:
            index.append(i)
    n = random.randint(0, len(index)-1)
    return index[n]

def eraseRow(ticketsList, row):
    for j in xrange(len(ticketsList[row])):
        ticketsList[row][j] = 0

def eraseCol(ticketsList, col):
    for i in xrange(len(ticketsList)):
        ticketsList[i][col] = 0

def findLucky(ticketList):
    ball = []
    for i in xrange(len(ticketList)):
        ball.extend([i]*ticketList[i])
    lucky = random.randint(0, len(ball)-1)
    return ball[lucky]

def drawCompleted(ticketsList):
    for i in xrange(len(ticketsList)):
        for j in xrange(len(ticketsList[0])):
            if ticketsList[i][j] > 0:
                return False
    return True

def drawTickets(ticketsList, rooms, randomAssign):
    r = len(ticketsList)
    t = len(ticketsList[0])
    results = [None] * t
    remainedRooms = range(r)
    while not drawCompleted(ticketsList):
        ticketsNum = countTickets(ticketsList)
        room = indexMax(ticketsNum)
        pair = findLucky(ticketsList[room])
        results[pair] = rooms[room]
        eraseRow(ticketsList, room)
        eraseCol(ticketsList, pair)
        temp = remainedRooms.index(room)
        del remainedRooms[temp]
    if randomAssign:
        for i in xrange(len(results)):
            if results[i] == None:
                temp = random.randint(0, len(remainedRooms)-1)
                room = remainedRooms[temp]
                results[i] = rooms[room]
                del remainedRooms[temp]
    return results

def exportResults(results, teams):
    t = len(teams)
    matrix = []
    for i in xrange(t):
        matrix.append(teams[i] + [results[i]])
    f = open('result.csv', 'wb')
    cw = csv.writer(f, delimiter=',')
    for i in xrange(len(matrix)):
        cw.writerow(matrix[i])
    f.close()

def exportSQL(results, teams):
    f = open('SQL.txt', 'w')
    for i in xrange(len(teams)):
        r = results[i]
        if r != None:
            t1 = teams[i][1]
            sn1 = t1[3]+t1[4]+"-"+t1[5]+t1[6]+t1[7]
            if t1:
                f.write("UPDATE `gaonnuri`.`xe_dorm` SET `rno` = '%s' WHERE `xe_dorm`.`sid` = '%s';" % (r, sn1))
                f.write("\n")
            t2 = teams[i][2]
            sn2 = t2[3]+t2[4]+"-"+t2[5]+t2[6]+t2[7]
            if t2:
                f.write("UPDATE `gaonnuri`.`xe_dorm` SET `rno` = '%s' WHERE `xe_dorm`.`sid` = '%s';" % (r, sn2))
                f.write("\n")
    f.close()

def main():
    exec open('settings.txt', 'r').read()
    rooms = convert(roomsM, roomsF)
    teams = readCsv('team.csv')
    tno = [teams[i][0] for i in xrange(len(teams))]
    tickets = readCsv('data.csv')
    ticketsList = arrangeTickets(rooms, tno, tickets)
    results = drawTickets(ticketsList, rooms, randomAssign)
    exportResults(results, teams)
    exportSQL(results, teams)
    print "Room Assignment Completed!!!"

if __name__ == '__main__':
    main()
