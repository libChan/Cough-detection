# README

Automatically Cough Location and Detection System.

Structure:

```
----cough_detection\
    |----data\
    |    |----test\
    |    |    |----Cough\
    |    |    |----nonCough\
    |    |----train\
    |    |    |----Cough\
    |    |    |----nonCough\
    |----eval\
    |    |----data\				# evaluation data
    |    |----result\			# evaluation result
    |    |----eval_beamforimg.py
    |    |----eval_doa.py
    |    |----plot_bf.py
    |    |----plot_doa.py
    |    |----plot_snr.py
    |    |----plot_svm.py
	|----real_time_detection\	#on Kinect Azure
    |    |----audio.png
    |    |----doa.png
    |    |----doa.py
    |    |----stream.py
    |    |----view.html 
    |----svm.arff
    |----svmSMtemp 				#saved SVM model 
    |----svmSMtemp.arff
    |----svmSMtempMEANS
    |----train\			
    |    |----train.py			# train and test SVM 

```

- data: Include train set and test set in SVM model.
- eval: Simulation of DoA estimation, beamforming  and plot evaluation result.
- real_time_detection: Run `main.py` to start the real time detection through Kinect mic array. And run `view.html` to monitor the audio stream and DoA.
- train: train SVM model and plot the result on test set.

