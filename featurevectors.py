from PIL import Image
import numpy as np

# get landmarks based on sliding a window over a profile
def get_landmarks(profile):
    start = 0
    end = 0

    # initial value arrays for min and max
    max_val = [0] * len(profile)
    min_val = [0] * len(profile)
    max_index = [0] * len(profile)
    min_index = [0] * len(profile)

    # slide the window and decide minimum and maximum values
    for i in range(len(profile)):
        win_start = max(0, i - 2)
        win_end = min(len(profile) - 1, i + 2)
        profile_win = profile[win_start : win_end + 1]
        max_val[i] = max(profile_win)
        max_index[i] = win_start + profile_win.index(max_val[i])
        min_val[i] = min(profile_win)
        min_index[i] = win_start + profile_win.index(min_val[i])

    # decide Ps and Pe
    for k in range(len(profile)):
        for i in range(len(profile)):
            if i != k:
                if min_index[k] > max_index[k]:
                    if (max_val[k] - min_val[k]) > (max_val[i] - min_val[i]):
                        # if the difference between max and min at k is greater than the difference
                        # of max and min at start, set start to k
                        if (max_val[k] - min_val[k]) > (max_val[start] - min_val[start]):
                            start = k
                if max_index[k] > min_index[k]:
                    if (max_val[k] - min_val[k]) > (max_val[i] - min_val[i]):
                        # if the difference between max and min at k is greater than the difference
                        # of max and min at end, set start to k
                        if (max_val[k] - min_val[k]) > (max_val[end] - min_val[end]):
                            end = k

    # create a landmark vector with
    # end - start is the number of pixels that the feature takes up                        
    landmark_vector = (start, end)
    return landmark_vector

def set_points(lines):
    # manually set two points along each line

    points = []
    for i in range(len(lines)):
        x1 = lines[i][0][0]
        x2 = lines[i][1][0]
        y1 = lines[i][0][1]
        y2 = lines[i][1][1]
        
        # use the slope to get points that fall along the line
        slope = (y2 - y1) / (x2 - x1)
        # define 2 points along this line, store the slope and intercept with the point for later use
        point1 = (round((-40 / slope) + x1), round(y1 - 40), slope)
        point2 = (round((-80 / slope) + x1), round(y1 - 80), slope)
        
        # adjust the above points as needed
        points.append(point1)
        points.append(point2)

    return points

def get_profiles(points, img_gray, out_img):
    # get the grayscale intensity profiles for the
    # axes perpendicular to each point
    profiles = []
    profile_img = img_gray
    for point in points:
        profile = []
        for i in range(-21, 24):
            slope = point[2]
            x = round(point[0] + i)
            # using the negative inverse slope for a perpendicular axis
            y = round(-(i / slope) + point[1]) 
            if x >= 0 and x < img_gray.width:
                if y >= 0 and y <= img_gray.height:
                    # go along the line perpendicular to the point and extract grayscale values
                    profile.append(img_gray.getpixel((x, y)))
                    profile_img.putpixel((x, y), 0)
        profiles.append(profile)

    profile_img.save(out_img)
    return profiles

def get_finger_widths(img_gray, lines, prof_img):
    # get finger widths

    # get the points along each line
    points = set_points(lines)

    # get the grayscale intensity profiles for the
    # axes perpendicular to each point
    profiles = get_profiles(points, img_gray, prof_img)

    # get landmarks for each of the profiles using the sliding window method
    landmarks = []
    for profile in profiles:
        landmarks.append(get_landmarks(profile))

    # calculate the distances by getting the difference between Ps and Pe
    distances = []
    for landmark in landmarks:
        distance = landmark[1] - landmark[0]
        distances.append(distance)

    return distances


def main():
    # load an image and convert to grayscale
    # img 1:
    img1 = Image.open("Image1.JPG")
    img1_gray = img1.convert("L")

    # manually define lines along the fingers
    lines1 = [
        ((75, 182), (31, 35)),
        ((113, 159), (127, 0)),
        ((152, 153), (193, 0)),
        ((194, 169), (259, 27))
    ]


    img1_distances = get_finger_widths(img1_gray, lines1, "Profiles1.JPG")
    print("Image1 distances:")
    for distance in img1_distances:
        print(distance)
    print("")

    img2 = Image.open("Image2.JPG")
    img2_gray = img2.convert("L")

    lines2 = [
        ((87, 177), (45, 40)),
        ((124, 161), (135, 0)),
        ((159, 159), (199, 0)),
        ((203, 166), (267, 20))
    ]

    img2_distances = get_finger_widths(img2_gray, lines2, "Profiles2.JPG")
    print("Image2 distances:")
    for distance in img2_distances:
        print(distance)
    print("")
    
    img3 = Image.open("Image3.JPG")
    img3_gray = img3.convert("L")

    lines3 = [
        ((97, 172), (53, 34)),
        ((131, 162), (144, 0)),
        ((164, 156), (205, 0)),
        ((207, 167), (274, 21))
    ]

    img3_distances = get_finger_widths(img3_gray, lines3, "Profiles3.JPG")
    print("Image3 distances:")
    for distance in img3_distances:
        print(distance)
    print("")

    img4 = Image.open("Image4.JPG")
    img4_gray = img4.convert("L")

    lines4 = [
        ((98, 173), (55, 36)),
        ((133, 159), (145, 0)),
        ((168, 157), (207, 0)),
        ((207, 167), (277, 27))
    ]

    img4_distances = get_finger_widths(img4_gray, lines4, "Profiles4.JPG")
    print("Image4 distances:")
    for distance in img3_distances:
        print(distance)
    print("")

    img5 = Image.open("Image5.JPG")
    img5_gray = img5.convert("L")

    lines5 = [
        ((98, 175), (54, 38)),
        ((132, 163), (144, 0)),
        ((166, 159), (206, 5)),
        ((208, 165), (273, 26))
    ]

    img5_distances = get_finger_widths(img5_gray, lines5, "Profiles5.JPG")
    print("Image5 distances:")
    for distance in img3_distances:
        print(distance)
    print("")

    # do a comparison between everything by finding mean and standard deviations
    print("Mean distances:")
    for i in range(len(img1_distances)):
        print(np.mean([
            img1_distances[i],
            img2_distances[i],
            img3_distances[i],
            img4_distances[i],
            img5_distances[i]
        ]))


    print("\nStandard deviations:")
    for i in range(len(img1_distances)):
        print(np.std([
            img1_distances[i],
            img2_distances[i],
            img3_distances[i],
            img4_distances[i],
            img5_distances[i]
        ]))


    

if __name__ == "__main__":
    main()