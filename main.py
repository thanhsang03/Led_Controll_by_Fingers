# import các module cần thiết
import cv2
import mediapipe as mp # nhận dạng và theo dõi các điểm đặc trưng trên tay
import time 
# import controller as cnt
import serial # giao tiếp qua cổng serial
import time

time.sleep(2.0) # Ct đợi 2s để làm việc tiếp

# khởi tạo đối tượng mediapipe  
# vẽ và nhận dạng các điểm đặc trưng trên tay
mp_draw=mp.solutions.drawing_utils 
mp_hand=mp.solutions.hands

tipIds=[4,8,12,16,20] # danh sách số đỉnh của ngón tay trên tay

video=cv2.VideoCapture(0) # mở wedcam or camera

# khởi tạo cổng serial kết nối vs Arduino
ArduinoUnoSerial = serial.Serial('COM3',9600) #create Serial object *REMEMBER to check the number of COM
print(ArduinoUnoSerial.readline()) #read the serial data and print it as line
print("You have new message from Arduino")

with mp_hand.Hands(min_detection_confidence=0.5, # khởi tạo đối tượng Hand từ module mp_hand
               min_tracking_confidence=0.5) as hands: # ngưỡng tối thiểu và tối đa
# with để tạo một ngữ cảnh (context) quản lý cho đối tượng hands. 
# Điều này đảm bảo rằng các tài nguyên liên quan đến hands sẽ được 
# giải phóng tự động khi kết thúc khối lệnh with, dù có xảy ra lỗi hay không.
    while True:
        ret,image=video.read() # đọc khung hình từ vd, ret xác nhận khung hình có được đọc chưa
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # chuyển đổi về màu RGB 
        image.flags.writeable=False # thiết lập thuộc tính writeable của img thành false 
        # ngăn chặn việc thay đổi nội dung của mảng hình ảnh này để đảm bảo tính nhất quán trong quá trình xử lý
        results=hands.process(image) # Sử dụng đối tượng hands để xử lý ảnh và 
        # nhận dạng các điểm đặc trưng trên tay. Kết quả được lưu trữ trong biến results
        image.flags.writeable=True # thành True để cho phép thay đổi nội dung của mảng
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # Chuyển đổi lại không gian màu của ảnh từ RGB sang BGR để sử dụng cho việc hiển thị hoặc lưu trữ.
        lmList=[] # Khởi tạo một danh sách rỗng để lưu trữ các điểm đặc trưng trên tay.
        if results.multi_hand_landmarks: # Kiểm tra xem có các đối tượng hand_landmark trên tay được nhận dạng trong kết quả hay không
            for hand_landmark in results.multi_hand_landmarks: # Lặp qua từng đối tượng hand_landmark trong danh sách các đối tượng multi_hand_landmarks.
                myHands=results.multi_hand_landmarks[0] # Lấy đối tượng myHands từ đối tượng multi_hand_landmarks đầu tiên. 
                #Trong trường hợp này, chỉ xem xét tay đầu tiên được nhận dạng.
                for id, lm in enumerate(myHands.landmark): # Lặp qua từng điểm đặc trưng (landmark) trong đối tượng myHands.
                    h,w,c=image.shape # Lấy chiều cao (h), chiều rộng (w), và số kênh màu (c) của ảnh.
                    cx,cy= int(lm.x*w), int(lm.y*h) # Tính toán tọa độ x và y của điểm đặc trưng (lm) dựa trên tọa độ tương đối và kích thước của ảnh.
                    # lm.x và lm.y là tọa độ tương đối của điểm đặc trưng theo trục x và trục y, 
                    # trong khoảng từ 0 đến 1. Điểm (0, 0) tương ứng với góc trên cùng bên trái của ảnh, và điểm (1, 1) tương ứng với góc dưới cùng bên phải của ảnh.
                    # w là chiều rộng của ảnh.
                    # h là chiều cao của ảnh.
                    lmList.append([id,cx,cy]) # Thêm một danh sách con chứa thông tin về id, tọa độ x và tọa độ y của điểm đặc trưng vào danh sách lmList
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS) #  Vẽ các điểm đặc trưng trên tay và các kết nối giữa chúng
        fingers=[] # Khởi tạo một danh sách rỗng để lưu trữ trạng thái của các ngón tay.
        if len(lmList)!=0: # Kiểm tra xem danh sách lmList chứa các điểm đặc trưng của tay có rỗng hay không. 
            # Nếu danh sách không rỗng, tiến hành xử lý các điểm đặc trưng để tính toán số ngón tay.
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            # So sánh tọa độ x của điểm đầu ngón tay cái (tipIds[0]) với tọa độ x của điểm ngay phía trước nó (tipIds[0]-1). 
            # Nếu tọa độ x của điểm ngón tay cái lớn hơn tọa độ x của điểm phía trước nó, tức là ngón tay cái giương lên, 
            # ta thêm số 1 vào danh sách fingers, ngược lại, thêm số 0.
            else:
                fingers.append(0)
            for id in range(1,5): # Duyệt qua các ngón tay từ ngón áp út (index 1) đến ngón cái (index 4).
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                    # ánh tọa độ y của điểm đầu ngón tay (tipIds[id]) với tọa độ y của điểm nằm ngay trên nó (tipIds[id]-2). 
                    # Nếu tọa độ y của điểm đầu ngón tay nhỏ hơn tọa độ y của điểm nằm trên nó, tức là ngón tay đó được giương lên, 
                    # ta thêm số 1 vào danh sách fingers, ngược lại, thêm số 0.
                else:
                    fingers.append(0)
            total=fingers.count(1) # đếm số ngón tay được giương lên và lưu vào biến total.
            # cnt.led(total)
            if total==0:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED) # Vẽ một hình chữ nhật màu xanh lá cây trên hình ảnh image, với tọa độ góc trên trái là (20, 300) và góc dưới phải là (270, 425).
                cv2.putText(image, "0", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5) #  Đặt văn bản "0" lên hình ảnh image, với vị trí góc trên trái của văn bản là (45, 375), font chữ là FONT_HERSHEY_SIMPLEX, kích thước font là 2, màu chữ là màu xanh dương (255, 0, 0) và độ dày là 5.
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5) # Đặt văn bản "LED" lên hình ảnh image, với vị trí góc trên trái của văn bản là (100, 375), font chữ là FONT_HERSHEY_SIMPLEX, kích thước font là 2, màu chữ là màu xanh dương (255, 0, 0) và độ dày là 5.
                ArduinoUnoSerial.write('0'.encode()) #send 1 to the arduino's Data code,  Gửi dữ liệu '0' (dạng mã ASCII) đến Arduino thông qua kết nối serial.
                print("0")
                time.sleep(1) 
            elif total==1:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "1", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                ArduinoUnoSerial.write('1'.encode()) #send 0 to the arduino's Data code
                print("1")
                time.sleep(1)
            elif total==2:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "2", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                ArduinoUnoSerial.write('2'.encode()) #send 0 to the arduino's Data code
                print("2")
                time.sleep(1)
            elif total==3:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "3", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                ArduinoUnoSerial.write('3'.encode()) #send 0 to the arduino's Data code
                print("3")
                time.sleep(1)
            elif total==4:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "4", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                ArduinoUnoSerial.write('4'.encode()) #send 0 to the arduino's Data code
                print("4")
                time.sleep(1)
            elif total==5:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "5", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                ArduinoUnoSerial.write('5'.encode()) #send 0 to the arduino's Data code
                print("5")
                time.sleep(1)
        cv2.imshow("Frame",image)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break         
video.release()
cv2.destroyAllWindows()

