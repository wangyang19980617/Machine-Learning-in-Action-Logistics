import numpy as np

def load_data_set():
    """
    加载数据集
    :return:返回两个数组，普通数组
        data_arr -- 原始数据的特征
        label_arr -- 原始数据的标签，也就是每条样本对应的类别
    """
    data_arr=[]
    label_arr=[]
    f=open('TestSet.txt','r')
    for line in f.readlines():
        line_arr=line.strip().split()
        #为了方便计算，我们将x0的值设为1.0，也就是在每一行的开头添加一个1.0，作为x0
        data_arr.append([1.0,np.float(line_arr[0]),np.float(line_arr[1])])
        label_arr.append(int(line_arr[2]))
    return data_arr,label_arr


def sigmoid(x):
    return 1.0/(1+np.exp(-x))

def grad_ascent(data_arr,class_labels):
    """
    梯度上升法，其实就是因为使用了极大似然估计，这个大家有必要去看推导，只看代码感觉不太够
    :param data_arr: 传入的就是一个普通的数组，当然你传入一个二维的ndarray也行
    :param class_labels: class_labels 是类别标签，它是一个 1*100 的行向量。
                    为了便于矩阵计算，需要将该行向量转换为列向量，做法是将原向量转置，再将它赋值给label_mat
    :return:
    """
    data_mat=np.mat(data_arr)
    #变成矩阵之后进行转置
    label_mat = np.mat(class_labels).transpose()
    #获得数据的样本量和特征维度数
    m,n=np.shape(data_mat)
    #学习率
    alpha=0.001
    #最大迭代次数
    max_cycles=500
    # 生成一个长度和特征数相同的矩阵，此处n为3 -> [[1],[1],[1]]
    # weights 代表回归系数， 此处的 ones((n,1)) 创建一个长度和特征数相同的矩阵，其中的数全部都是 1
    weights = np.ones((n, 1))
    for k in range(max_cycles):
        h=sigmoid(data_mat*weights)
        error=label_mat-h
        weights=weights+alpha*data_mat.transpose()*error
    return weights



def plot_best_fit(weights):
    """
    可视化
    :param weights:
    :return:
    """
    import matplotlib.pyplot as plt
    data_mat, label_mat = load_data_set()
    data_arr = np.array(data_mat)
    n = np.shape(data_mat)[0]
    x_cord1 = []
    y_cord1 = []
    x_cord2 = []
    y_cord2 = []
    for i in range(n):
        if int(label_mat[i]) == 1:
            x_cord1.append(data_arr[i, 1])
            y_cord1.append(data_arr[i, 2])
        else:
            x_cord2.append(data_arr[i, 1])
            y_cord2.append(data_arr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_cord1, y_cord1, s=30, color='k', marker='^')
    ax.scatter(x_cord2, y_cord2, s=30, color='red', marker='s')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    """
    y的由来，卧槽，是不是没看懂？
    首先理论上是这个样子的。
    dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
    w0*x0+w1*x1+w2*x2=f(x)
    x0最开始就设置为1叻， x2就是我们画图的y值，而f(x)被我们磨合误差给算到w0,w1,w2身上去了
    所以： w0+w1*x+w2*y=0 => y = (-w0-w1*x)/w2   
    """
    ax.plot(x, y)
    plt.xlabel('x1')
    plt.ylabel('y1')
    plt.show()




def test():
    """
    这个函数只要就是对上面的几个算法的测试，这样就不用每次都在power shell 里面操作，不然麻烦死了
    :return:
    """
    data_arr, class_labels = load_data_set()
    # 注意，这里的grad_ascent返回的是一个 matrix, 所以要使用getA方法变成ndarray类型
    weights = grad_ascent(data_arr, class_labels).getA()
    # weights = stoc_grad_ascent0(np.array(data_arr), class_labels)
    #weights = stoc_grad_ascent1(np.array(data_arr), class_labels)
    plot_best_fit(weights)

# ---------------------真实训练数据和测试数据-------从疝气病症预测病马的死亡率------


def classify_vector(in_x, weights):
    """
    最终的分类函数，根据回归系数和特征向量来计算 Sigmoid 的值，大于0.5函数返回1，否则返回0
    :param in_x: 特征向量，features
    :param weights: 根据梯度下降/随机梯度下降 计算得到的回归系数
    :return:
    """
    # print(np.sum(in_x * weights))
    prob = sigmoid(np.sum(in_x * weights))
    if prob > 0.5:
        return 1.0
    return 0.0


def stoc_grad_ascent1(data_mat, class_labels, num_iter=150):
    """
    改进版的随机梯度上升，使用随机的一个样本来更新回归系数
    :param data_mat: 输入数据的数据特征（除去最后一列）,ndarray
    :param class_labels: 输入数据的类别标签（最后一列数据
    :param num_iter: 迭代次数
    :return: 得到的最佳回归系数
    """
    m, n = np.shape(data_mat)
    weights = np.ones(n)
    for j in range(num_iter):
        # 这里必须要用list，不然后面的del没法使用
        data_index = list(range(m))
        for i in range(m):
            # i和j的不断增大，导致alpha的值不断减少，但是不为0
            alpha = 4 / (1.0 + j + i) + 0.01
            # 随机产生一个 0～len()之间的一个值
            # random.uniform(x, y) 方法将随机生成下一个实数，它在[x,y]范围内,x是这个范围内的最小值，y是这个范围内的最大值。
            rand_index = int(np.random.uniform(0, len(data_index)))
            h = sigmoid(np.sum(data_mat[data_index[rand_index]] * weights))
            error = class_labels[data_index[rand_index]] - h
            weights = weights + alpha * error * data_mat[data_index[rand_index]]
            del(data_index[rand_index])
    return weights



def colic_test():
    """
    打开测试集和训练集，并对数据进行格式化处理,其实最主要的的部分，比如缺失值的补充（真的需要学会的），人家已经做了
    :return:
    """
    f_train = open('HorseColicTraining.txt', 'r')
    f_test = open('HorseColicTest.txt', 'r')
    training_set = []
    training_labels = []
    # 解析训练数据集中的数据特征和Labels
    # trainingSet 中存储训练数据集的特征，trainingLabels 存储训练数据集的样本对应的分类标签
    for line in f_train.readlines():
        curr_line = line.strip().split('\t')
        if len(curr_line) == 1:
            continue    # 这里如果就一个空的元素，则跳过本次循环
        line_arr = [float(curr_line[i]) for i in range(21)]
        training_set.append(line_arr)
        training_labels.append(float(curr_line[21]))
    # 使用 改进后的 随机梯度下降算法 求得在此数据集上的最佳回归系数 trainWeights
    train_weights = stoc_grad_ascent1(np.array(training_set), training_labels, 500)
    error_count = 0
    num_test_vec = 0.0
    # 读取 测试数据集 进行测试，计算分类错误的样本条数和最终的错误率
    for line in f_test.readlines():
        num_test_vec += 1
        curr_line = line.strip().split('\t')
        if len(curr_line) == 1:
            continue    # 这里如果就一个空的元素，则跳过本次循环
        line_arr = [float(curr_line[i]) for i in range(21)]
        #预测结果claaify_vector
        if int(classify_vector(np.array(line_arr), train_weights)) != int(curr_line[21]):
            error_count += 1
    error_rate = error_count / num_test_vec
    print('the error rate is {}'.format(error_rate))
    return error_rate



if __name__ == '__main__':
    #test()
    colic_test()