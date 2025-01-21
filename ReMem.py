import os
import random
import time
from tkinter import Tk, Label, PhotoImage
from threading import Thread, Event
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from dotenv import load_dotenv
from PIL import Image, ImageTk



SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class ImageWindow:
    def __init__(self):
        self.root = None
        self.close_event = Event()

    def close_window(self):
        if self.root:
            # Schedule window closure on the main thread using after()
            self.root.after(0, self._close_window)

    def _close_window(self):
        # This function will be called in the main event loop
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None
            self.close_event.set()

    def display_image(self, image_path):
        self.close_event.clear()
        self.root = Tk()
        self.root.title("Current Prompt Image")
        
        # Normalize the image path
        image_path = os.path.normpath(image_path)  # Ensure correct path format
        
        # Make window fullscreen and always on top
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        
        # Disable window close button
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Open image using Pillow and convert it for Tkinter
        img = Image.open(image_path)
        img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        
        # Convert image to Tkinter format
        img_tk = ImageTk.PhotoImage(img)
        
        # Create label with black background
        label = Label(self.root, image=img_tk, bg='black')
        label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Keep reference to image to prevent garbage collection
        label.image = img_tk
        
        # Start window in separate thread
        self.root.mainloop()


def authenticate_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def get_file_list(service, folder_id):
    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="files(id, name)",
            orderBy='modifiedTime desc'
        ).execute()
        return results.get('files', [])
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

class ImageTracker:
    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.shown_images = set()
        self.all_images = set(os.listdir(image_folder))
    
    def get_next_image(self):
        available_images = self.all_images - self.shown_images
        
        # If all images have been shown, reset the tracking
        if not available_images:
            print("\nAll images have been shown. Resetting tracking...")
            self.shown_images.clear()
            available_images = self.all_images
        
        # Choose random image from available ones
        next_image = random.choice(list(available_images))
        self.shown_images.add(next_image)
        return next_image

def main():
    load_dotenv()  
    image_folder = os.getenv("IMAGE_FOLDER")
    google_drive_folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    
    service = authenticate_google_drive()
    print("Google Drive authentication successful.")
    
    image_tracker = ImageTracker(image_folder)
    image_window = ImageWindow()

    while True:
        # Get next random image (no repeats until all shown)
        random_image = image_tracker.get_next_image()
        image_path = os.path.join(image_folder, random_image)
        print(f"\nDisplaying image: {random_image}")
        
        # Start image display in separate thread
        display_thread = Thread(target=image_window.display_image, args=(image_path,))
        display_thread.start()
        
        # Get initial state of Drive folder
        initial_files = get_file_list(service, google_drive_folder_id)
        initial_count = len(initial_files)
        print(f"Current files in Drive folder: {initial_count}")
        print("Waiting for new file to be uploaded...")
        
        # Monitor for changes
        while True:
            time.sleep(5)  # Check every 5 seconds
            current_files = get_file_list(service, google_drive_folder_id)
            current_count = len(current_files)

            if current_count > initial_count:
                new_files = [f for f in current_files if f['id'] not in [file['id'] for file in initial_files]]
                if new_files:
                    print(f"New file detected: {new_files[0]['name']}")
                    # Close the image window (this will now safely happen on the main thread)
                    image_window.close_window()
                    display_thread.join()  # Wait for window thread to finish
                    
                    print("Starting one hour wait period...")
                    time.sleep(3600)  
                    print("One hour has passed. Starting next cycle...\n")
                    break

if __name__ == '__main__':
    main()
