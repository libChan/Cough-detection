from pyAudioAnalysis import audioTrainTest as aT

aT.extract_features_and_train(["../data/train/Cough", "../data/train/nonCough"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep,
                            "svm_rbf", "../svmSMtemp", False)
cm, thr_pre, pre, rec, thr_roc, fpr, tpr = aT.evaluate_model_for_folders(["../data/test/Cough", "../data/test/nonCough"],
                                                                         "../svmSMtemp", "svm_rbf", "Cough")
print('Training over....')
