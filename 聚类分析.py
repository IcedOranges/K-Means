import math
import time
import random
import matplotlib.pyplot as plt

class KMeans:
    def __init__(self, k, pointsAcount, dataRange):
        self.k = int(k)
        self.pointsAcount = int(pointsAcount)
        self.dataRange = int(dataRange)
        self.dataset = []
        self.startPooints = []

    def generateDataset(self):
        Xs = []
        Ys = []
        a = 0
        while a < self.pointsAcount:
            Xs.append(random.randint(0, self.dataRange))
            Ys.append(random.randint(0, self.dataRange))
            a += 1
        self.dataset.append(Xs)
        self.dataset.append(Ys)
        return self.dataset

    @staticmethod
    def distanceFormula(point1, point2):
        distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        return distance

    @staticmethod
    def getMin(compareList):
        minNum = compareList[0]
        minIndex = 0
        for i in range(len(compareList)):
            if compareList[i] < minNum:
                minNum = compareList[i]
                minIndex = i
        return minNum, minIndex

    def randomStart(self):
        newDataset = self.dataset.copy()
        newDataset.append([])
        a = 0
        print() # 格式控制
        while a < self.k:
            positon = random.randint(0, self.pointsAcount - 1)
            newDataset[2].append([newDataset[0][positon], newDataset[1][positon]])
            a += 1
            print('起始中心点 {} 为： ( {:.5f} , {:.5f} )'.format(str(a), newDataset[0][positon], newDataset[1][positon]))
        return newDataset

    def generateClusters(self, newDataset):
        # 准备
        a = 0
        clusterList = []
        while a < self.k:
            clusterList.append([])
            a += 1

        # 计算各点到起始点的距离
        distanceDict = {}
        startPointIndex = 0
        for startPoint in newDataset[2]:
            distanceDict.setdefault(str(startPointIndex), [])
            for p in range(self.pointsAcount):
                if [newDataset[0][p], newDataset[1][p]] in newDataset[2]:
                    pass
                else:
                    anotherPoint = [newDataset[0][p], newDataset[1][p]]
                    distance = self.distanceFormula(startPoint, anotherPoint)
                    distanceDict[str(startPointIndex)].append(distance)
            startPointIndex += 1

        # 比较各点到起始点距离，近的归为一簇
        for p in range(self.pointsAcount-self.k):
            compareList = []
            for k in range(self.k):
                compareList.append(distanceDict[str(k)][p])
            minDistance, minIndex = self.getMin(compareList)
            clusterList[minIndex].append(p)

        # 计算各簇平均值点
        newDataset[2].clear()
        a = 0
        for cluster in clusterList:
            Xs = 0
            Ys = 0
            for p in cluster:
                Xs += newDataset[0][p]
                Ys += newDataset[1][p]
            newStartPoint = [Xs/len(cluster), Ys/len(cluster)]
            newDataset[2].append(newStartPoint)
            a += 1
            print('新的中心点 {} 为： ( {:.5f} , {:.5f} )'.format(str(a), Xs/len(cluster), Ys/len(cluster)))
        return newDataset[2], clusterList

    @staticmethod
    def randomColor():
        colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ''
        for i in range(6):
            color += colorArr[random.randint(0, 14)]
        return '#' + color

    def drawDataset(self, startPointList, clusterList):
        plt.title('K-Means Clustering Results')
        plt.xlabel('X')
        plt.ylabel('Y')
        for startPoint in startPointList:
            startPointColor = self.randomColor()
            plt.plot(startPoint[0], startPoint[1], color=startPointColor, marker='o')
            for cluster in clusterList:
                pointColor = self.randomColor()
                for p in cluster:
                    plt.plot(self.dataset[0][p], self.dataset[1][p], color=pointColor, marker='.')
        plt.show()

    def runKMeans(self):
        startTime = time.time()

        self.generateDataset()

        newDataset = self.randomStart()
        lastStartPointList = []
        print('\n开始第 1 次迭代...')
        newStartPointList, clusterList = self.generateClusters(newDataset)
        iteration = 2
        while lastStartPointList != newStartPointList:
            print('\n开始第 ' + str(iteration) + ' 次迭代...')
            newDataset = self.dataset.copy()
            newDataset.append(newStartPointList)
            lastStartPointList = newStartPointList.copy()
            newStartPointList, clusterList = self.generateClusters(newDataset)
            iteration += 1
        print() # 格式控制
        k = 0
        while k < self.k:
            print('迭代完毕，最终中心点 {} 为： ( {:.5f} , {:.5f} )'.format(str(k+1), newStartPointList[k][0], newStartPointList[k][1]))
            k += 1

        endTime = time.time()
        print('\n共耗费时间： ' + str(endTime-startTime))

        self.drawDataset(newStartPointList, clusterList)

if __name__ == '__main__':
    # dataRange表示坐标轴长度刻度最大值
    KMeans = KMeans(
        k=input('请输入K值：'),
        pointsAcount=input('请输入随机点个数：'),
        dataRange=input('请输入坐标轴最大刻度：')
    )
    KMeans.runKMeans()
