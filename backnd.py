from ultralytics import YOLO
import cv2
import time
import os
from PyQt6.QtCore import QThread, pyqtSignal

print("backnd started")
class Video_summarizer(QThread):
    # Define a signal to emit progress
    update_progress = pyqtSignal(int)
    # Define a signal to indicate completion
    finished = pyqtSignal(int, int)

    def __init__(self,video_path):
        super().__init__()
        self.video_path = video_path
        self.device = "cpu"
        self.model = YOLO("yolov8n.pt").to(self.device)
        self.vid_speed = 2

    def run(self):
        start = time.time()

        cap = cv2.VideoCapture(self.video_path)
        assert cap.isOpened(), "Error reading video file"

        # Get the video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Get the total number of frames
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = 'output/output1.mp4'
        output_folder = 'output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        i=0
        frame_count = 0
        inc=1
        flag=0
        no_obj=0
        prev_progress = -1
        num_objects=0

        

        # for(i=i+1,)
        while cap.isOpened():
            success, im0 = cap.read()

            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break

            i=i+1
            if i%self.vid_speed != 0 :
                continue
            
            results = self.model.track(im0, device='cpu', verbose=False, conf=0.5, persist=True)  # Tracking recommended
            annotated_frame = results[0].plot() if results else im0.copy()
            
            # if len(results) != 0:
            num_objects = len(results[0].boxes) if results else None

            if num_objects!=0:
                flag = True
                out.write(annotated_frame)
                
            #print(num_objects)
            if flag == 1 and num_objects==0:
                no_obj=no_obj+1
                # print(no_obj)
                if no_obj>2:
                    inc +=1
                    flag=0
                    no_obj=0
                    output_path = f"output/output{inc}.mp4"
                    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
            
            if i == total_frames:
                inc +=1
                flag=0
                no_obj=0
                output_path = f"output/output{inc}.mp4"
                out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

            #progress tracking
            progress = int(i * 100 / total_frames)
            if progress % 5 == 0 and progress != prev_progress:
                print(f"{progress}%")
                prev_progress = progress
            
            self.update_progress.emit(progress)  # Emit progress signal

            # cv2.imshow("frame", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if out is not None:
            out.release()

        cap.release()
        cv2.destroyAllWindows()

        stop = time.time()
        print(f"time taken : {(stop - start):.2f}")
        print("completed")


        self.finished.emit(inc-1, self.video_path)  # Emit finished signal when done

