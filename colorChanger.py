import numpy as np
import cv2

HUE = 1
VALUE = 2


def change_hv(src, hue_or_value, num, lower, upper):
    """
    :param src: source image
    :param hue_or_value: channel to change, hue = 1, value = 2
    :param num: amount to add to hue or value
    :param lower: lower limit to range of color
    :param upper: upper limit to range of color
    :return: changed image
    """
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    # black and white
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('mask', mask)
    # colored
    res_mask = cv2.bitwise_and(src, src, mask=mask)
    h, s, v = cv2.split(cv2.cvtColor(res_mask, cv2.COLOR_BGR2HSV))
    if hue_or_value == 1:
        h = np.mod(h + num, 180).astype(np.uint8)
    elif hue_or_value == 2:
        v = np.clip(v - num, 0, 255).astype(np.uint8)
    else:
        return 'wrong input'
    merged = cv2.cvtColor(cv2.merge([h, s, v]), cv2.COLOR_HSV2BGR)
    img1_bg = cv2.bitwise_and(src, src, mask=cv2.bitwise_not(mask))
    cv2.imshow('back', img1_bg)
    img2_fg = cv2.bitwise_and(merged, merged, mask=mask)
    cv2.imshow('frnt', img2_fg)
    res = cv2.add(img1_bg, img2_fg)
    return res


def main():
    lower_blue = np.array([95, 50, 50])
    upper_blue = np.array([130, 255, 255])

    lower_green = np.array([30, 50, 50])
    upper_green = np.array([80, 255, 255])

    img = cv2.resize(cv2.imread("prague.jpg"), (0, 0), None, .50, .50)

    blue_red = change_hv(img, HUE, 80, lower_blue, upper_blue)
    green_bright = change_hv(blue_red, VALUE, 100, lower_green, upper_green)

    result = np.hstack((img, green_bright))
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
