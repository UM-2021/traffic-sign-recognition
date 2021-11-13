import my_classification as train
from joblib import dump


clf_red = train.train_red()
# clf_yellow = train.train_yellow()
dump(clf_red, './trained_models/red_training.joblib') 
# dump(clf_yellow, 'yellow_training.joblib') 