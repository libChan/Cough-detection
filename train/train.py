from pyAudioAnalysis import audioTrainTest as aT

# train svm
aT.extract_features_and_train(["../data/train/Cough", "../data/train/nonCough"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep,
                            "svm_rbf", "../svmSMtemp", False)
print('Training over....')
# test svm and plot the evaluation
cm, thr_pre, pre, rec, thr_roc, fpr, tpr = aT.evaluate_model_for_folders(["../data/test/Cough", "../data/test/nonCough"],
                                                                         "../svmSMtemp", "svm_rbf", "Cough")
