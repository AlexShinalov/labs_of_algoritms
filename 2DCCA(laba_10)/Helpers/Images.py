import cv2
import os
import numpy as np

class Images:
    @staticmethod
    def get_links(num_test: int = 1, all: bool = False, dataset: str = "dataset_old") -> tuple[list, list]:

        links_x = list()
        links_y = list()
        if all: 
            links_xy = list()
            for i in range(5):
                links_xy = Images.get_links(i + 1)
                links_x += links_xy[0]
                links_y += links_xy[1]
        else:      
            k = 0
            for directory in os.listdir(f"{dataset}/termal"):
                if os.path.isfile(f"{dataset}/termal/{directory}/{num_test}.jpg"):
                    links_x.append(f"{dataset}/termal/{directory}/{num_test}.jpg")
                    links_y.append(f"{dataset}/visible/{directory}/{num_test}.jpg")
        return links_x, links_y
    
    @staticmethod
    def resize_and_crop(image: np.ndarray, target_width: int = 10, target_height: int = 10, isheight: bool = True) -> np.ndarray:
        original_height, original_width = image.shape
        aspect_ratio = original_width / original_height

        if isheight:
            new_height = target_height
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = target_width
            new_height = int(new_width / aspect_ratio)

        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        image = np.clip(image, 0, 255).astype(np.uint8)

        return image
    
    def sharpen_image(image_path: str, new_image_path: str) -> None:
        image = cv2.imread(image_path)

        # Define the sharpening kernel
        sharpen_filter = np.array([[-1, -1, -1],
                                   [-1, 9, -1],
                                   [-1, -1, -1]])

        sharpened_image = cv2.filter2D(image, -1, sharpen_filter)
        cv2.imwrite(new_image_path, sharpened_image)
        
    @staticmethod
    def get_pictures(links) -> np.ndarray:
        result = list()
        for filename in links:
            imageX = cv2.imread(filename, 0)
            img = np.float64(imageX) / 255
            result.append(img)
        return np.array(result)
    
    @staticmethod
    def get_links_for_gui(link: str) -> list[str]:
        links_termal = list()
        links_visible = list()
        
        for directory in os.listdir(f"{link}/termal"):
            for filename in os.listdir(f"{link}/termal/{directory}"):
                links_termal.append(f"{link}/termal/{directory}/{filename}")

            for filename in os.listdir(f"{link}/visible/{directory}"):
                links_visible.append(f"{link}/visible/{directory}/{filename}")
            
        return links_termal, links_visible
            
    