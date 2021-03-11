


def normalize_data(train_data, test_data, type=None):
    if type == 'standard':
        scaler = preprocessing.StandardScaler()
    elif type == 'l1':
        scaler = preprocessing.Normalizer(norm='l1')
    elif type == 'l2':
        scaler = preprocessing.Normalizer(norm='l2')

    scaler.fit(train_data)
    scalat1 = scaler.transform(train_data)
    scalat2 = scaler.transform(test_data)

    return (scalat1, scalat2)


class BagOfWords:

    def __init__(self):
        self.vocabular = {}
        self.l = []
        self.id = 0

    def build_vocabulary(self, data):
        for eseu in data:
            for cuvant in eseu:
                if cuvant not in self.vocabular.keys():
                    self.vocabular[cuvant] = self.id
                    self.id += 1
                    self.l.append(cuvant)


def get_features(self, data):
    features = np.zeros((len(data), self.id))
    id_sample = -1
    for sample in data:
        id_sample += 1
        for word in sample:
            if word in self.vocabular.keys():
                features[id_sample][self.vocabular[word]] += 1
    return features


bow = BagOfWords()
bow.build_vocabulary(train_data)
print(bow.get_size())
train = bow.get_features(train_data)
test = bow.get_features(test_data)
normalized_train, normalized_test = normalize_data(train, test, 'f2')

model = svm.SVC(C=1, kernel='linear')
model.fit(normalized_train, train_y)

predict = model.predict(normalized_test)

print(accuracy_score(test_y, predict))
print(f1_score(test_y, predict))
