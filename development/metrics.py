def precision_at_k(y_true, y_pred, k):
    """
    Precision at k
    :param y_true: list of true labels
    :param y_pred: list of predicted labels
    :param k: number of top k elements to consider
    :return: precision at k
    """
    if len(y_pred) > k:
        y_pred = y_pred[:k]
    return round(len(set(y_true) & set(y_pred)) / len(y_pred), 2)

def recall_at_k(y_true, y_pred, k):
    """
    Recall at k
    :param y_true: list of true labels
    :param y_pred: list of predicted labels
    :param k: number of top k elements to consider
    :return: recall at k
    """
    if len(y_pred) > k:
        y_pred = y_pred[:k]
    return round(len(set(y_true) & set(y_pred)) / len(y_true), 2)

