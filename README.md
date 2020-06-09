# README

Automatically Cough Location and Detection System.

### **Dependency**

```
pip install -r requirements.txt
```

Run all python scripts(except for doa.py) through command:

```
python *.py 
eg. python eval_beamforming.py 
```

(tested in python 3.7)

### Project Structure

- data: Include train dataset and datatest set in SVM model.

- eval: 

  `eval_beamforming.py`: Beamforming evaluation. Set the cough sound as interest signal, white noise as interference signal. Compute the time domain MVDR filter. Output: SNR before and after MVDR filter processing.

  `eval_doa.py`: evaluate the impact of different sources' azimuth and distance on DoA estimation, as well as SNR.

  `plot_bf.py`: plot the result of beamforming evaluation(azimuth and distance).

  `plot_doa.py`: plot the result of DoA estimation.

  `plot_snr.py`: plot the result of beamforming evaluation(SNR). 

  `plot_svm.py`: plot the result of SVM_linear and SVM_RBF model.

- real_time_detection: 

   `main.py` : real time cough detection through Kinect mic array. 

   `view.html`:  to monitor the audio stream and DoA estimation result.

- train: 

  `train.py`: train SVM model on train dataset. Plot the result on test set.

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
