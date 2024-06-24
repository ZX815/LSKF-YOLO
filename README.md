# SRSPTD Dataset Used in LSKF-YOLO
This project provides a power tower image data subset, named SRSPTD, obtained from the Electric Transmission and Distribution Infrastructure imagery Dataset re-cropped and annotated
## Electric Transmission and Distribution Infrastructure Imagery Dataset
* This dataset comprises fully annotated high-resolution satellite and aerial images of transmission and distribution infrastructure, encompassing an area of approximately 321 square kilometers  across  14  cities  in 6  countries  on  5  continents.
 It covers diverse terrain types and human settlement densities.   
* Data Availability : The dataset used in this study is supported by the Bass Connections Project of Duke University, USA. The datasets can be accessed from https://figshare.com/articles/Electric_Transmission_and_Distribution_Infrastructure_Imagery_Dataset/6931088.
### SRSPTD Dataset
* the paper focuses on images from four states in the United States (Turson - AZ, Hartford-CT, Colwich&Maize - KS, and Wilmington - NC), as well as images from Taranga and Dunedin, New Zealand, obtained from LINZ, Austria, which form a subset of the data. The images from these six selected regions respectively represent four types of terrain: desert, plain, forest, and coastal, and three types of human habitation density areas: suburban, rural, and urban.  
* The original images in the dataset had resolutions ranging from 3800 to 12000 pixels, and some had an aspect ratio that made direct training impractical. To better suit the model's training requirements, all subset images were cropped from top to bottom and left to right to 512?512 images. Additionally, since the original dataset's annotations were in polygon format, which was not suitable for the target detection model, we used labelImg to re-annotate the images, categorizing annotations into transmission towers and distribution towers.
As the distribution towers were challenging to observe in satellite images, their own shadows were labeled as a unit with themselves during the annotation process to provide more information to the model.
![SRSPTD Dataset]()
#### 
 
