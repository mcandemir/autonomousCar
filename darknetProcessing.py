import argparse
import os
import glob
import random
import darknet
import time
import cv2
import numpy as np
import darknet
from PIL import ImageGrab

class DarknetProcessing:

    def __init__(self, trafficSign):
        self.trafficSign = trafficSign
        self.args = self.parser()
        self.check_arguments_errors(self.args)

        random.seed(3)  # deterministic bbox colors
        self.network, self.class_names, self.class_colors = darknet.load_network(
            self.args.config_file,
            self.args.data_file,
            self.args.weights,
            batch_size=self.args.batch_size
        )

        images = self.load_images(self.args.input)

    def parser(self):
        parser = argparse.ArgumentParser(description="YOLO Object Detection")
        parser.add_argument("--input", type=str, default="",
                            help="image source. It can be a single image, a"
                            "txt with paths to them, or a folder. Image valid"
                            " formats are jpg, jpeg or png."
                            "If no input is given, ")
        parser.add_argument("--batch_size", default=1, type=int,
                            help="number of images to be processed at the same time")
        parser.add_argument("--weights", default="./yolov4-tiny-custom_flip0_best_86_3xxx.weights",
                            help="yolo weights path")
        parser.add_argument("--dont_show", action='store_true',
                            help="windown inference display. For headless systems")
        parser.add_argument("--ext_output", action='store_true',
                            help="display bbox coordinates of detected objects")
        parser.add_argument("--save_labels", action='store_true',
                            help="save detections bbox for each image in yolo format")
        parser.add_argument("--config_file", default="./yolov4-tiny-custom_flip0.cfg",
                            help="path to config file")
        parser.add_argument("--data_file", default="./data/yolov4-tiny.data",
                            help="path to data file")
        parser.add_argument("--thresh", type=float, default=.70,
                            help="remove detections with lower confidence")
        return parser.parse_args()


    def check_arguments_errors(self, args):
        assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
        if not os.path.exists(args.config_file):
            raise(ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
        if not os.path.exists(args.weights):
            raise(ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
        if not os.path.exists(args.data_file):
            raise(ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))
        if args.input and not os.path.exists(args.input):
            raise(ValueError("Invalid image path {}".format(os.path.abspath(args.input))))


    def check_batch_shape(self, images, batch_size):
        """
            Image sizes should be the same width and height
        """
        shapes = [image.shape for image in images]
        if len(set(shapes)) > 1:
            raise ValueError("Images don't have same shape")
        if len(shapes) > batch_size:
            raise ValueError("Batch size higher than number of images")
        return shapes[0]


    def load_images(self, images_path):
        """
        If image path is given, return it directly
        For txt file, read it and return each line as image path
        In other case, it's a folder, return a list with names of each
        jpg, jpeg and png file
        """
        input_path_extension = images_path.split('.')[-1]
        if input_path_extension in ['jpg', 'jpeg', 'png']:
            return [images_path]
        elif input_path_extension == "txt":
            with open(images_path, "r") as f:
                return f.read().splitlines()
        else:
            return glob.glob(
                os.path.join(images_path, "*.jpg")) + \
                glob.glob(os.path.join(images_path, "*.png")) + \
                glob.glob(os.path.join(images_path, "*.jpeg"))


    def prepare_batch(self, images, network, channels=3):
        width = darknet.network_width(network)
        height = darknet.network_height(network)

        darknet_images = []
        for image in images:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_resized = cv2.resize(image_rgb, (width, height),
                                    interpolation=cv2.INTER_LINEAR)
            custom_image = image_resized.transpose(2, 0, 1)
            darknet_images.append(custom_image)

        batch_array = np.concatenate(darknet_images, axis=0)
        batch_array = np.ascontiguousarray(batch_array.flat, dtype=np.float32)/255.0
        darknet_images = batch_array.ctypes.data_as(darknet.POINTER(darknet.c_float))
        return darknet.IMAGE(width, height, channels, darknet_images)


    def image_detection(self, image_path, network, class_names, class_colors, thresh):
        # Darknet doesn't accept numpy images.
        # Create one with image we reuse for each detect
        
        image = cv2.imread(image_path)
        width = image.shape[1]
        height = image.shape[0]
        darknet_image = darknet.make_image(width, height, 3)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image_rgb, (width, height),
                                interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
        darknet.free_image(darknet_image)
        image = darknet.draw_boxes(detections, image_resized, class_colors)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections


    def batch_detection(self, network, images, class_names, class_colors,
                        thresh=0.25, hier_thresh=.5, nms=.45, batch_size=4):
        image_height, image_width, _ = check_batch_shape(images, batch_size)
        darknet_images = self.prepare_batch(images, network)
        batch_detections = darknet.network_predict_batch(network, darknet_images, batch_size, image_width,
                                                        image_height, thresh, hier_thresh, None, 0, 0)
        batch_predictions = []
        for idx in range(batch_size):
            num = batch_detections[idx].num
            detections = batch_detections[idx].dets
            if nms:
                darknet.do_nms_obj(detections, num, len(class_names), nms)
            predictions = darknet.remove_negatives(detections, class_names, num)
            images[idx] = darknet.draw_boxes(predictions, images[idx], class_colors)
            batch_predictions.append(predictions)
        darknet.free_batch_detections(batch_detections, batch_size)
        return images, batch_predictions


    def image_classification(self, image, network, class_names):
        width = darknet.network_width(network)
        height = darknet.network_height(network)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image_rgb, (width, height), interpolation=cv2.INTER_LINEAR)
        darknet_image = darknet.make_image(width, height, 3)
        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
        detections = darknet.predict_image(network, darknet_image)
        predictions = [(name, detections[idx]) for idx, name in enumerate(class_names)]
        darknet.free_image(darknet_image)
        return sorted(predictions, key=lambda x: -x[1])


    def convert2relative(self, image, bbox):
        """
        YOLO format use relative coordinates for annotation
        """
        x, y, w, h = bbox
        height, width, _ = image.shape
        return x/width, y/height, w/width, h/height


    def save_annotations(self, name, image, detections, class_names):
        """
        Files saved with image_name.txt and relative coordinates
        """
        file_name = name.split(".")[:-1][0] + ".txt"
        with open(file_name, "w") as f:
            for label, confidence, bbox in detections:
                x, y, w, h = convert2relative(image, bbox)
                label = class_names.index(label)
                f.write("{} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(label, x, y, w, h, float(confidence)))


    def batch_detection_example(self):
        args = parser()
        check_arguments_errors(args)
        batch_size = 3
        random.seed(3)  # deterministic bbox colors
        network, class_names, class_colors = darknet.load_network(
            args.config_file,
            args.data_file,
            args.weights,
            batch_size=batch_size
        )
        image_names = ['data/horses.jpg', 'data/horses.jpg', 'data/eagle.jpg']
        images = [cv2.imread(image) for image in image_names]
        images, detections,  = self.batch_detection(network, images, class_names,
                                            class_colors, batch_size=batch_size)
        for name, image in zip(image_names, images):
            cv2.imwrite(name.replace("data/", ""), image)
        print(detections)


    def process(self, ss):
        """
        index = 0
        while True:
            prev_time = time.time()
            ss = ImageGrab.grab((0, 0, 1500, 900))
            img_np = np.array(ss)
            im_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            cv2.imwrite("temp.jpg", im_rgb)
            # loop asking for new image paths if no list is given
            image, detections = self.image_detection(
                "temp.jpg", self.network, self.class_names, self.class_colors, self.args.thresh
                )
            if self.args.save_labels:
                self.save_annotations(image_name, image, detections, class_names)
            darknet.print_detections(detections, self.args.ext_output)
            print(detections)
            trafficSign = TrafficSign()
            if detections != []:
                for x in detections:
                    if x[0] == "ileriSol":
                        trafficSign.trafficSignArray[2] = 1
                        cv2.imshow("ileriSol", image[int(x[2][3]):int(x[2][0]), int(x[2][2]):int(x[2][1])])
            else:
                trafficSign.trafficSignArray[2] = 0
            trafficSign.printingAllSigns()

            fps = int(1/(time.time() - prev_time))
            print("FPS: {}".format(fps))
            if not self.args.dont_show:
                cv2.imshow('Inference', image)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            index += 1

        """
        #ss = ImageGrab.grab((0, 0, 1500, 900))
        img_np = np.array(ss)
        im_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        cv2.imwrite("temp.jpg", im_rgb)
        # loop asking for new image paths if no list is given
        image, detections = self.image_detection(
            "temp.jpg", self.network, self.class_names, self.class_colors, self.args.thresh
            )
        if self.args.save_labels:
            self.save_annotations(image_name, image, detections, class_names)
        darknet.print_detections(detections, self.args.ext_output)
        #print(detections)
        #return detections
        if detections != []:
            for x in detections:
                if x[0] == "park":
                    self.trafficSign.trafficSignArray[0] = 1
                else:
                    self.trafficSign.trafficSignArray[0] = 0
                if x[0] == "parkYasak":
                    self.trafficSign.trafficSignArray[1] = 1
                else:
                    self.trafficSign.trafficSignArray[1] = 0
                if x[0] == "durak":
                    self.trafficSign.trafficSignArray[2] = 1
                else:
                    self.trafficSign.trafficSignArray[2] = 0
                if x[0] == "sol":
                    self.trafficSign.trafficSignArray[3] = 1
                else:
                    self.trafficSign.trafficSignArray[3] = 0
                if x[0] == "sag":
                    self.trafficSign.trafficSignArray[4] = 1
                else:
                    self.trafficSign.trafficSignArray[4] = 0
                if x[0] == "solaDonulmez":
                    self.trafficSign.trafficSignArray[5] = 1
                else:
                    self.trafficSign.trafficSignArray[5] = 0
                if x[0] == "sagaDonulmez":
                    self.trafficSign.trafficSignArray[6] = 1
                else:
                    self.trafficSign.trafficSignArray[6] = 0
                if x[0] == "ileriSol":
                    self.trafficSign.trafficSignArray[7] = 1
                else:
                    self.trafficSign.trafficSignArray[7] = 0
                if x[0] == "ileriSag":
                    self.trafficSign.trafficSignArray[8] = 1
                else:
                    self.trafficSign.trafficSignArray[8] = 0
                if x[0] == "dur":
                    self.trafficSign.trafficSignArray[9] = 1
                else:
                    self.trafficSign.trafficSignArray[9] = 0
                if x[0] == "30":
                    self.trafficSign.trafficSignArray[10] = 1
                else:
                    self.trafficSign.trafficSignArray[10] = 0
                if x[0] == "20":
                    self.trafficSign.trafficSignArray[11] = 1
                else:
                    self.trafficSign.trafficSignArray[11] = 0
                if x[0] == "yesil":
                    self.trafficSign.trafficSignArray[12] = 1
                if x[0] == "kirmizi":
                    self.trafficSign.trafficSignArray[12] = 0
                if x[0] == "girisYok":
                    self.trafficSign.trafficSignArray[13] = 1
                else:
                    self.trafficSign.trafficSignArray[13] = 0
                if x[0] == "tasitTrafigineKapali":
                    self.trafficSign.trafficSignArray[14] = 1
                else:
                    self.trafficSign.trafficSignArray[14] = 0
        else:
            self.trafficSign.trafficSignArray[0] = 0
            self.trafficSign.trafficSignArray[1] = 0
            self.trafficSign.trafficSignArray[2] = 0
            self.trafficSign.trafficSignArray[3] = 0
            self.trafficSign.trafficSignArray[4] = 0
            self.trafficSign.trafficSignArray[5] = 0
            self.trafficSign.trafficSignArray[6] = 0
            self.trafficSign.trafficSignArray[7] = 0
            self.trafficSign.trafficSignArray[8] = 0
            self.trafficSign.trafficSignArray[9] = 0
            self.trafficSign.trafficSignArray[10] = 0
            self.trafficSign.trafficSignArray[11] = 0
            self.trafficSign.trafficSignArray[12] = -1
            self.trafficSign.trafficSignArray[13] = 0
            self.trafficSign.trafficSignArray[14] = 0

                    #cv2.imshow("ileriSol", image[int(x[2][3]):int(x[2][0]), int(x[2][2]):int(x[2][1])])
                    #cv2.imshow("ileriSol", image[int(x[2][3]):int(x[2][0]), int(x[2][2]):int(x[2][1])])
        self.trafficSign.printingAllSigns()
        if not self.args.dont_show:
            cv2.imshow('Inference', image)

        

"""
if __name__ == "__main__":
    # unconmment next line for an example of batch processing
    # batch_detection_example()
    main()"""
