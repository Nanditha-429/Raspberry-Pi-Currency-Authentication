from picamera2 import Picamera2
import cv2
import time
from RPLCD.i2c import CharLCD

lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2,
    charmap='A02'
)

lcd.clear()
lcd.write_string("Currency Check")
lcd.cursor_pos = (1, 0)
lcd.write_string("Initializing")
time.sleep(2)


def resize_img(img, scale=0.6):
    w = int(img.shape[1] * scale)
    h = int(img.shape[0] * scale)
    return cv2.resize(img, (w, h))


def uv_feature_score(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # UV fluorescence color range
    lower_uv = (80, 40, 40)
    upper_uv = (140, 255, 255)

    mask = cv2.inRange(hsv, lower_uv, upper_uv)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bright = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    uv_mask = cv2.bitwise_and(mask, bright)

    score = cv2.countNonZero(uv_mask)

    return score, uv_mask


# CAMERA CAPTURE
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

time.sleep(2)

lcd.clear()
lcd.write_string("Capturing...")

test_img = picam2.capture_array()
picam2.stop()

cv2.imwrite("files/test.jpg", test_img)

display_img = resize_img(test_img)


# ORB INITIALIZATION
orb = cv2.ORB_create(nfeatures=1500)
kp1, des1 = orb.detectAndCompute(test_img, None)


# ORB TRAINING SET
orb_training = [
    "files/train_100_1.jpg",
    "files/train_100_2.jpg",
    "files/train_100_3.jpg",
    "files/train_100_4.jpg",
    "files/train_200_1.jpg",
    "files/train_200_2.jpg",
    "files/train_200_3.jpg",
    "files/train_200_4.jpg",
    "files/train_500_1.jpg",
    "files/train_500_2.jpg",
    "files/train_500_3.jpg",
    "files/train_500_4.jpg"
]

max_matches = 0
best_orb_note = None

for path in orb_training:
    train_img = cv2.imread(path)

    kp2, des2 = orb.detectAndCompute(train_img, None)

    if des1 is None or des2 is None:
        continue

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    matches = bf.knnMatch(des1, des2, k=2)

    good = []

    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    if len(good) > max_matches:
        max_matches = len(good)
        best_orb_note = path.split("_")[1]


# UV TRAINING SET
uv_training = {
    "100": [
        "files/uv_100_1.jpg",
        "files/uv_100_2.jpg",
        "files/uv_100_3.jpg",
        "files/uv_100_4.jpg"
    ],
    "200": [
        "files/uv_200_1.jpg",
        "files/uv_200_2.jpg",
        "files/uv_200_3.jpg",
        "files/uv_200_4.jpg"
    ],
    "500": [
        "files/uv_500_1.jpg",
        "files/uv_500_2.jpg",
        "files/uv_500_3.jpg",
        "files/uv_500_4.jpg"
    ]
}

test_uv_score, uv_mask = uv_feature_score(test_img)

best_uv_note = None
best_diff = 1e9

for note, imgs in uv_training.items():
    scores = []

    for img_path in imgs:
        img = cv2.imread(img_path)
        score, _ = uv_feature_score(img)
        scores.append(score)

    avg_score = sum(scores) / len(scores)

    diff = abs(test_uv_score - avg_score)

    if diff < best_diff:
        best_diff = diff
        best_uv_note = note


ORB_THRESHOLD = 30
UV_THRESHOLD = 5000

if (
    max_matches >= ORB_THRESHOLD
    and test_uv_score >= UV_THRESHOLD
    and best_orb_note == best_uv_note
):
    lcd.clear()
    lcd.write_string("GENUINE NOTE")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(best_orb_note)

    text = f"GENUINE NOTE {best_orb_note}"
    color = (0, 255, 0)

else:
    lcd.clear()
    lcd.write_string("FAKE NOTE")

    text = "FAKE NOTE"
    color = (0, 0, 255)


cv2.putText(
    display_img,
    text,
    (30, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    color,
    3
)

cv2.imshow("Currency Detection", display_img)
cv2.imshow("UV Mask", uv_mask)

cv2.waitKey(4000)
cv2.destroyAllWindows()

lcd.cursor_pos = (1, 0)
time.sleep(2)

lcd.clear()
lcd.write_string("Done")
