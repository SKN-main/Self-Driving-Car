import time
import cv2
from Direction import Direction
from Car import Car


inputWidth = 1280
inputHeight = 720
inputFrameRate = 60

rescaledWidth = 848
rescaledHeight = 480


def main():
    car = Car()
    cap = cv2.VideoCapture(0)

    action = None
    prev_action = '0-0'

    i = 0

    is_finish = False
    while not is_finish:
        _, image = cap.read()

        mask, frame_with_road_sign, direction, turn_value = car(image)
        
        if direction.value == Direction.STRAIGHT.value and prev_action[0] != 'w':
            print(f'{i}. straight')
            action = 'w-0'
            time.sleep(0.05)
        elif direction.value == Direction.RIGHT.value and prev_action != f'd-{turn_value}':
            print(f'{i}. right {turn_value}')
            action = f'd-{turn_value}'
            time.sleep(0.05)
        elif direction.value == Direction.LEFT.value and prev_action != f'a-{turn_value}':
            print(f'{i}. left {turn_value}')
            action = f'a-{turn_value}'
            time.sleep(0.05)

        cv2.imshow('Mask', mask)
        cv2.imshow('Frame', frame_with_road_sign)

        key = cv2.waitKey(10) & 0xFF

        if key == ord('q'):
            is_finish = True

        prev_action = action
        i+= 1


if __name__ == '__main__':
    main()


