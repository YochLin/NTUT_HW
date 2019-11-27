from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


if __name__ == '__main__':
    with open('Practice05_Data.txt', 'r') as f:
        data = [items.replace('\n', "").split('\t') for items in f]
        data = [[float(i) for i in each[1:-1]] for each in data]

    kmeans = KMeans(n_clusters=7, init='random', n_init=1)
    kmeans = kmeans.fit(data)

    labels = kmeans.predict(data)
    centroids = kmeans.cluster_centers_
    print(centroids)

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter([i[0]for i in data],[i[1]for i in data],[i[3]for i in data], c=labels)
    # ax.scatter([i[0]for i in centroids], [i[1]for i in centroids], [i[3]for i in centroids], c='r')
    plt.show()

    # plt.figure()
    # plt.scatter([i[0]for i in data], [i[1]for i in data])
    # plt.scatter([i[0]for i in centroids], [i[1]for i in centroids])
    # plt.title('R & G')
    # plt.xlabel('R')
    # plt.ylabel('G')
    # plt.figure()
    # plt.scatter([i[0]for i in data], [i[2]for i in data])
    # plt.scatter([i[0]for i in centroids], [i[2]for i in centroids])
    # plt.title('R & B')
    # plt.xlabel('R')
    # plt.ylabel('B')
    # plt.figure()
    # plt.scatter([i[0]for i in data], [i[3]for i in data])
    # plt.scatter([i[0]for i in centroids], [i[3]for i in centroids])
    # plt.title('R & H')
    # plt.xlabel('R')
    # plt.ylabel('H')
    # plt.figure()
    # plt.scatter([i[1]for i in data], [i[2]for i in data])
    # plt.scatter([i[1]for i in centroids], [i[2]for i in centroids])
    # plt.title('G & B')
    # plt.xlabel('G')
    # plt.ylabel('B')
    # plt.figure()
    # plt.scatter([i[1]for i in data], [i[3]for i in data])
    # plt.scatter([i[1]for i in centroids], [i[3]for i in centroids])
    # plt.title('G & H')
    # plt.xlabel('G')
    # plt.ylabel('H')
    # plt.figure()
    # plt.scatter([i[2]for i in data], [i[3]for i in data])
    # plt.scatter([i[2]for i in centroids], [i[3]for i in centroids])
    # plt.title('B & H')
    # plt.xlabel('B')
    # plt.ylabel('H')
    # plt.show()
    