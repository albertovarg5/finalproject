# Final Project

## Description

My final project will be a web application where users can upload an image and apply different image processing effects. The user will be able to choose between multiple effects such as grayscale, blur, edge detection, and color inversion. The application will process the image using OpenCV and display the result on a web page. I will build it using Python, Flask, OpenCV, and Docker. The goal is to create a simple and interactive tool for experimenting with image effects.

## Design

For this project, I am starting with the Docker template from class because it already provides a working Flask application that can run in a container and be deployed later. My plan is to keep the basic image upload flow from the template and then extend the image processing part so the user can choose from several effects instead of only one. In the first prototype, I want to make sure the user can upload an image, select an effect, submit the form, and see the processed result displayed on the web page.

I am approaching this project one step at a time. First, I will get one effect working correctly, such as grayscale or blur. After that, I will add more effects like edge detection and color inversion. OpenCV will be used to read and modify the images, Flask will handle the web page and file upload, and Docker will make sure the program runs the same way on my computer and on Render. During development, I may improve the layout of the page so it is easier for the user to understand and use.

Websites used:
- OpenCV Python Tutorials: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- Flask Documentation: https://flask.palletsprojects.com/
- GeeksforGeeks OpenCV Project Ideas: https://www.geeksforgeeks.org/computer-vision/opencv-projects-ideas-for-beginners/

AI usage:
I used ChatGPT to help me brainstorm a project idea, improve my README description, and plan the design of the application. I asked for help choosing an easy but strong project idea, deciding which image effects to include, and understanding how the Flask upload page and OpenCV image processing should work together. I may continue using AI during development for debugging, documentation help, and improving the structure of the code.

## Implementation

I implemented my project by modifying the template into a web application that allows users to upload an image and apply different image processing effects. The user can choose between grayscale, blur, edge detection, and invert colors. The app displays both the original and processed image on the web page.

I used Flask to handle the web interface and OpenCV to process the images. I also created folders for uploads and outputs so that images can be saved and displayed correctly. The application runs locally in the browser and successfully processes images based on user input.

AI usage:
I used ChatGPT to help me modify the template, add multiple image effects, fix errors, and improve my code structure and documentation.