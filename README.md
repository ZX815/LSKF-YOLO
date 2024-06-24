# SRSPTD Dataset Used in LSKF-YOLO
This project provides a power tower image data subset, named SRSPTD, obtained from the Electric Transmission and Distribution Infrastructure imagery Dataset re-cropped and annotated  
If this dataset is helpful to your research, please cite our article in the citation format:  
C. Shi, X. Zheng, Z. Zhao, K. Zhang, Z. Su and Q. Lu, "LSKF-YOLO: Large Selective Kernel Feature Fusion Network for Power Tower Detection in High-Resolution Satellite Remote Sensing Images," in IEEE Transactions on Geoscience and Remote Sensing, vol. 62, pp. 1-16, 2024, Art no. 5620116, doi: 10.1109/TGRS.2024.3389056. 
## Electric Transmission and Distribution Infrastructure Imagery Dataset
* This dataset comprises fully annotated high-resolution satellite and aerial images of transmission and distribution infrastructure, encompassing an area of approximately 321 square kilometers  across  14  cities  in 6  countries  on  5  continents. It covers diverse terrain types and human settlement densities.   
* Data Availability : The dataset used in this study is supported by the Bass Connections Project of Duke University, USA. The datasets can be accessed from https://figshare.com/articles/Electric_Transmission_and_Distribution_Infrastructure_Imagery_Dataset/6931088.
### SRSPTD Dataset
* the paper focuses on images from four states in the United States (Turson - AZ, Hartford-CT, Colwich&Maize - KS, and Wilmington - NC), as well as images from Taranga and Dunedin, New Zealand, obtained from LINZ, Austria, which form a subset of the data. The images from these six selected regions respectively represent four types of terrain: desert, plain, forest, and coastal, and three types of human habitation density areas: suburban, rural, and urban.  
* The original images in the dataset had resolutions ranging from 3800 to 12000 pixels, and some had an aspect ratio that made direct training impractical. To better suit the model's training requirements, all subset images were cropped from top to bottom and left to right to 512*512 images.
* Additionally, since the original dataset's annotations were in polygon format, which was not suitable for the target detection model, we used labelImg to re-annotate the images, categorizing annotations into transmission towers and distribution towers. As the distribution towers were challenging to observe in satellite images, their own shadows were labeled as a unit with themselves during the annotation process to provide more information to the model.
![SRSPTD Dataset]()
#### Project file description
* SRSPTD Dataset： This folder provides datasets in yolo annotated format that can be divided as needed
* SRSPTD(VOC): This file provides a data set in VOC format, with the training set, verification set, and test set divided into 7:2:1 ratios
* SRSPTD（5-k cross _val) : The file provides a 5-k cross-validation dataset in YOLO format, with a training set to validation set ratio of 8:2
* Dataset Processing：This folder provides some data set format conversion, partition code files
  If you have any question about this dataset, feel free to contact zheng_xian0815@163.com/220222215007@ncepu.edu.cn.

 
