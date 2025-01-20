

# Image Display with Google Drive Integration

This program randomly displays images from a folder on your computer in fullscreen mode. The images are displayed one at a time, and the program waits for new files to be uploaded to a specific Google Drive folder. When a new file is uploaded, the program will wait for an hour before starting a new cycle of displaying images.

## What You Need

Before you begin, make sure you have these:

- **Python 3.6+** installed on your computer.
- **Google Drive API credentials** (We’ll get to that in a moment).
- A folder on your computer where you store the images you want to display.
- The **Google Drive folder ID** where files will be monitored for uploads.

## Setting Up the Project

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```

### 2. Install Dependencies

You will need to install a few Python libraries. Run this command in your terminal to install them:

```bash
pip install -r requirements.txt
```

This will install the required libraries like `google-api-python-client`, `tkinter`, `python-dotenv`, etc.

### 3. Get Google API Credentials

To authenticate with Google Drive, you need to enable the Google Drive API and get a **credentials.json** file.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the Google Drive API for the project.
4. Create OAuth 2.0 credentials, download the **credentials.json** file, and save it in the same folder as your Python script.

### 4. Set Up Environment Variables

Create a `.env` file in your project folder to store sensitive information:

```env
IMAGE_FOLDER=path/to/your/images
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id
```

Replace `path/to/your/images` with the folder where you store images on your computer, and `your_google_drive_folder_id` with the ID of your Google Drive folder.

To find your Google Drive folder ID:

- Open your folder on Google Drive.
- Copy the part of the URL that comes after `folders/`. For example: `https://drive.google.com/drive/folders/your_folder_id`.

### 5. Running the Program

Now that everything is set up, you can run the program with:

```bash
python ReMem.py
```

### 6. How It Works

- The program loads and displays random images from your local folder in fullscreen mode.
- Images are displayed one at a time, and after all images have been shown, the tracker resets.
- The program monitors the specified Google Drive folder for new file uploads.
- When a new file is uploaded to the folder, the program waits for **one hour** before continuing the cycle and showing a new random image.

## Troubleshooting

- If the image does not display, check the file path in your `.env` file.
- Ensure you’ve correctly set up Google API credentials by checking the `credentials.json` file.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Mykal-Steele/ReMem/blob/main/LICENSE) file for details.
