

Real-time visual traffic objection and car distance approximation system

This project presents a real-time visual traffic object detection and car distance approximation system, leveraging the YOLO simulator for simulation in realistic urban maps. After evaluating several popular detection models, YOLO was chosen due to its superior balance of speed and accuracy, despite unsuccessful attempts at further acceleration through parallel processing. A custom dataset was generated using traffic-related images collected via web scraping and an automated image capture tool developed in the CARLA simulator. These images were labeled manually to train the YOLO model for enhanced detection capabilities in diverse traffic scenarios. For distance approximation, a reference-based calculation system was devised, utilizing stop sign dimensions and Wikipedia-scraped vehicle specifications, coupled with a MobileNetV2-based vehicle classification model. The system integrates both detection and distance approximation into a unified environment using a custom Pygame-based interface, facilitating testing and development. This work advances real-time, robust object detection and distance measurement in autonomous driving systems.


![image](https://github.com/user-attachments/assets/4758ca2a-56c5-4120-b75e-fa2462b9e600)





![image](https://github.com/user-attachments/assets/9ba6e4af-1f5e-4962-8646-f2c3aa4732aa)

![image](https://github.com/user-attachments/assets/bb6cc952-cabe-4e36-b19c-615a1087ce62)




![image](https://github.com/user-attachments/assets/18093f08-c341-434f-8c67-0aec85aec5ad)



