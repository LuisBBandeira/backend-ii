import os
from queue import Queue
import threading
import time
from PIL import Image, ImageFilter
import logging

class ImageProcessor:
    def __init__(self, input_dir="input", output_dir="output", num_workers=4):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.image_queue = Queue()
        self.num_workers = num_workers
        self.workers = []
        self.running = False
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
      
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_image(self, image_file):
       
        try:
            
            img_path = os.path.join(self.input_dir, image_file)
            img = Image.open(img_path)
            
           
            img = img.filter(ImageFilter.SHARPEN)
            img = img.filter(ImageFilter.EDGE_ENHANCE)
            
           
            output_path = os.path.join(self.output_dir, f"processed_{image_file}")
            img.save(output_path)
            
            logging.info(f"Processed {image_file} -> {output_path}")
            
        except Exception as e:
            logging.error(f"Error processing {image_file}: {str(e)}")
    
    def worker(self):
        
        while self.running:
            image_file = self.image_queue.get()
            if image_file is None:  
                self.image_queue.task_done()
                break
                
            self.process_image(image_file)
            self.image_queue.task_done()
    
    def start_workers(self):
       
        self.running = True
        for _ in range(self.num_workers):
            worker_thread = threading.Thread(target=self.worker)
            worker_thread.start()
            self.workers.append(worker_thread)
    
    def stop_workers(self):
       
        self.running = False
       
        for _ in range(self.num_workers):
            self.image_queue.put(None)
        
       
        for worker in self.workers:
            worker.join()
        
        self.workers = []
    
    def process_directory(self):
        try:
           
            image_files = [
                f for f in os.listdir(self.input_dir) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
            ]
            
            if not image_files:
                logging.warning(f"No images found in {self.input_dir}")
                return
            
           
            self.start_workers()
            
           
            for image_file in image_files:
                self.image_queue.put(image_file)
            
        
            self.image_queue.join()
            
            logging.info("Finished processing all images")
            
        finally:
            self.stop_workers()

if __name__ == "__main__":
    processor = ImageProcessor(
        input_dir="input_images",
        output_dir="output_images",
        num_workers=4
    )
    
    try:
        processor.process_directory()
    except KeyboardInterrupt:
        logging.info("Received keyboard interrupt, shutting down...")
        processor.stop_workers()