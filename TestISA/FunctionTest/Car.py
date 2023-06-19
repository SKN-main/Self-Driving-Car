import cv2
from LaneDetector import LaneDetector, Tracker
from RoadSignsDetector import RoadSignsDetector
from Direction import Direction
from Queue import Queue
from collections import Counter
from copy import deepcopy
import numpy as np


IMAGE_SIZE = (1280, 720)


class Car:
    def __init__(self, use_sign_detector=True, tracking=False) -> None:
        self.lane_detector = LaneDetector()
        self.left_tracker = Tracker((0.20, 0.7), 200)
        self.right_tracker = Tracker((0.80, 0.7), 200)
        self.direction = Direction.STRAIGHT
        self.turn = None
        self.recent_tracker = self.left_tracker
        self.sign_direction = None
        self.use_sign_detector = use_sign_detector
        self.tracking = tracking
        if use_sign_detector:
            self.road_signs_detector = RoadSignsDetector('20e_street_20e_printed.pt')
        self.possible_signs = Queue(8)
        self.possible_directions = Queue(10)
        self.prev_sign = None
        self.detected_sign = None
        self.car_direction = None

    def detect_road_sign(self, image):
        nearest_sign = None

        image = self.road_signs_detector.predict(image)
        signs = self.road_signs_detector.get_predicted_signs()

        nearest_signs = sorted(signs, key=lambda t: abs(t[1]-t[3])*abs(t[0]-t[2]))

        if len(nearest_signs):
            nearest_sign = nearest_signs[0][4]

        self.possible_signs.add(nearest_sign)

        most_common_sign = Counter(self.possible_signs.array).most_common()[0][0]

        if most_common_sign == 'c12':
            self.prev_sign = deepcopy(self.detected_sign)
            self.detected_sign = 'c12'
        elif most_common_sign == 'b20':
            self.prev_sign = deepcopy(self.detected_sign)
            self.detected_sign = 'b20'
        elif most_common_sign == 'c2':
            self.prev_sign = deepcopy(self.detected_sign)
            self.detected_sign = 'c2'
        elif most_common_sign == 'c4':
            self.prev_sign = deepcopy(self.detected_sign)
            self.detected_sign = 'c4'
        else:
            self.detected_sign = None
        
        return image


    def find_duck(self, frame):
        iou = 0
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([20, 120, 70])
        upper = np.array([30, 255, 255])

        mask1 = cv2.inRange(image, lower, upper)

        lower = np.array([20, 70, 70])
        upper = np.array([30, 255, 255])

        mask2 = cv2.inRange(image, lower, upper)

        mask = mask1 + mask2 
        blur = cv2.GaussianBlur(mask,(25,25),0)
        thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)[1]

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            iou += w*h/(frame.shape[0]*frame.shape[1])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 2)

        return iou


    def track_car(self, frame):
        biggest_iou = 0
        position_x = frame.shape[1]//2
        # print(position_x)
        direction = Direction.STRAIGHT
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array([78,158,124])
        upper = np.array([138,255,255])

        mask = cv2.inRange(image, lower, upper)

        blur = cv2.GaussianBlur(mask,(25,25),0)
        thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)[1]

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            iou = w*h/(frame.shape[0]*frame.shape[1])
            if iou > biggest_iou:
                biggest_iou = iou
                position_x = x+w//2
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 2)

        deviation = abs(position_x - frame.shape[1]//2)/(frame.shape[1]//2)

        if position_x < frame.shape[1]//2:
            direction = Direction.LEFT
        elif position_x > frame.shape[1]//2:
            direction = Direction.RIGHT

        return direction, deviation
    

    def straight(self):
        left_tracker_dir_val =  self.left_tracker.get_direction().value
        right_tracker_dir_val =  self.right_tracker.get_direction().value

        if Direction.STRAIGHT.value in [left_tracker_dir_val, right_tracker_dir_val]:
            self.direction = Direction.STRAIGHT

        elif left_tracker_dir_val == right_tracker_dir_val:
            self.direction = self.left_tracker.get_direction()

        elif self.recent_tracker is not None:
            self.direction = self.recent_tracker.get_direction()

        
    
    def __call__(self, frame):
        frame = cv2.resize(frame, IMAGE_SIZE)
        mask, direction = self.lane_detector(frame)


        if self.tracking:
            direction, turn_value = self.track_car(frame)
            turn_value = int(100*turn_value)
            
            if direction.value in [Direction.LEFT.value, Direction.RIGHT.value]:
                self.car_direction = direction
            elif direction.value == Direction.STRAIGHT.value and self.car_direction is None:
                self.car_direction = direction
            elif direction.value == Direction.STRAIGHT.value and self.car_direction is not None:
                turn_value = 100
            
            cv2.putText(frame, f"{self.car_direction.name}", (100, 100), 2, 3, (0, 0, 255), 2)
            cv2.putText(frame, f"{turn_value}", (100, 150), 2, 3, (0, 0, 255), 2)

            return mask, frame, self.car_direction, turn_value
        

        turn_value = 0

        if self.use_sign_detector:
            frame_with_road_sign = self.detect_road_sign(frame)

        self.left_tracker.track(mask)
        self.right_tracker.track(mask)

        if self.right_tracker.is_active:
            self.recent_tracker = self.right_tracker
        elif self.left_tracker.is_active:
            self.recent_tracker = self.left_tracker

        if direction is not None and direction.value != Direction.STRAIGHT.value:
            if self.turn:
                self.direction = self.turn
            else:
                # if direction.value == Direction.LEFT and not self.right_tracker.is_active:
                #     self.direction = Direction.LEFT
                #     self.turn = Direction.LEFT
                # elif direction.value == Direction.RIGHT and not self.left_tracker.is_active:
                #     self.direction = Direction.RIGHT
                #     self.turn = Direction.RIGHT

                if direction.value == Direction.LEFT:
                    self.direction = Direction.LEFT
                    self.turn = Direction.LEFT
                elif direction.value == Direction.RIGHT:
                    self.direction = Direction.RIGHT
                    self.turn = Direction.RIGHT

                self.direction = direction

            turn_value = 100
        else:
            if direction.value == Direction.LEFT.value:
                self.direction = Direction.LEFT
                self.recent_tracker = self.right_tracker
            elif direction.value == Direction.RIGHT.value:
                self.direction = Direction.RIGHT
                self.recent_tracker = self.left_tracker
            else:
                self.straight()
                self.turn = None
                turn_value = abs(int(self.recent_tracker.deviation//2))


        if (self.prev_sign == 'c12' or self.prev_sign == 'c2') and self.detected_sign is None:
            self.sign_direction = Direction.RIGHT
            if direction is not None or direction.value != Direction.STRAIGHT.value:
                self.direction = deepcopy(self.sign_direction)
                if self.right_tracker.is_active and self.right_tracker.get_direction().value == Direction.LEFT.value:
                    self.prev_sign = None
                    self.sign_direction = None

        if self.prev_sign == 'c4' and self.detected_sign is None:
            self.sign_direction = Direction.LEFT
            if direction is not None or direction.value != Direction.STRAIGHT.value:
                self.direction = deepcopy(self.sign_direction)
                if self.left_tracker.is_active and self.left_tracker.get_direction().value == Direction.RIGHT.value:
                    self.prev_sign = None
                    self.sign_direction = None

        if self.prev_sign == 'b20' and self.detected_sign is None:
            pass
            # stop the car

        iou = self.find_duck(frame)
        if iou > 0.2:
            self.direction = Direction.STOP


        cv2.putText(mask, self.direction.name, (500 ,500), 1, 3, (0, 0, 255), 3)
        if self.turn is not None:
            cv2.putText(mask, "Turn: " + self.turn.name, (500 ,550), 1, 3, (0, 0, 255), 3)

        if self.use_sign_detector:
            if self.detected_sign:
                cv2.putText(frame_with_road_sign, "sign: " + self.detected_sign, (500 ,600), 1, 3, (0, 0, 255), 3)
            if self.prev_sign:
                cv2.putText(frame_with_road_sign, "prev sign: " + self.prev_sign, (500 ,650), 1, 3, (0, 0, 255), 3)


        self.left_tracker.draw(mask)
        self.right_tracker.draw(mask)

        return mask, frame, self.direction, turn_value
        # return mask, frame_with_road_sign, self.direction, 100 if turn.value != Direction.STRAIGHT.value else 50
    