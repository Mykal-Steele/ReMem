# Image Display with Google Drive Integration

This program randomly displays images from a folder on your computer in fullscreen mode. The images are displayed one at a time, and the program waits for new files to be uploaded to a specific Google Drive folder. When a new file is uploaded, the program will wait for an hour before starting a new cycle of displaying images.

## What You Need

Before you begin, make sure you have the following:

- **Python 3.6+** installed on your computer.
- **Google Drive API credentials** (We'll guide you through the setup).
- A folder on your computer where you store the images you want to display.
- The **Google Drive folder ID** where files will be monitored for uploads.

## Setting Up the Project

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/Mykal-Steele/ReMem.git
cd ReMem
```

### 2. Install Dependencies

You will need to install a few Python libraries. Run this command in your terminal to install them:

```bash
pip install -r requirements.txt
```

This will install the required libraries such as `google-api-python-client`, `tkinter`, `python-dotenv`, etc.

### Optional: Set Up a Virtual Environment (Recommended)

It's a good practice to use a virtual environment. You can set it up like this:

#### For macOS/Linux:

```bash
python3 -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate the virtual environment
pip install -r requirements.txt  # Install dependencies
```

#### For Windows:

```bash
python -m venv venv  # Create a virtual environment
venv\Scripts\activate  # Activate the virtual environment
pip install -r requirements.txt  # Install dependencies
```

### 3. Get Google API Credentials

To authenticate with Google Drive, you need to enable the Google Drive API and get a `credentials.json` file.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the **Google Drive API** for the project:
   - Navigate to **APIs & Services > Library**.
   - Search for "Google Drive API" and enable it.
4. Set up the **OAuth consent screen**:
   - Go to **APIs & Services > OAuth consent screen**.
   - Select the **External** user type (unless you're testing with internal users).
   - Complete the required fields like app name, user support email, and developer contact email.
   - Under **Scopes**, add the scope `https://www.googleapis.com/auth/drive.readonly` (this will give the program read-only access to your Google Drive files).
   - In the **Test Users** section, add your Google account as a test user. This allows you to use the app during testing before it's fully approved by Google.
   - Click **Save and Continue** to finish the setup.
5. Create **OAuth 2.0 credentials**:
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials** and select **OAuth 2.0 Client IDs**.
   - Choose **Desktop App** as the application type.
   - Download the **Client Secret** file (it will be named something like `credentials.json`).
   - Save the `credentials.json` file in the same folder as your Python script.

Now, the application will use the `https://www.googleapis.com/auth/drive.readonly` scope to authenticate and access files in your Google Drive, and you can test it using your Google account as a test user.

### 4. Set Up Environment Variables

Create a `.env` file in your project folder to store sensitive information like the image folder path and Google Drive folder ID:

```env
IMAGE_FOLDER=path/to/your/images
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id
```

Replace `path/to/your/images` with the folder where you store images on your computer. Replace `your_google_drive_folder_id` with the ID of your Google Drive folder.

To find your Google Drive folder ID:

- Open your folder on Google Drive.
- Copy the part of the URL that comes after `folders/`. For example: `https://drive.google.com/drive/folders/your_folder_id`.

### 5. Running the Program

Now that everything is set up, you can run the program with:

```bash
python ReMem.py
```

### 6. How It Works

- The program loads and displays random images from your local folder in fullscreen mode, one at a time.
- The images remain on the screen until a new file is uploaded to the designated **Google Drive folder**.
- **To close the current fullscreen image and move to the next step**, you must upload any file (it doesn't have to be an image) to the specified Google Drive folder. Once a new file is uploaded:
  1. The program detects the upload and closes the fullscreen image.
  2. The program starts a **one-hour timer** before continuing with the next cycle.
- After the one-hour wait, the program will start showing a new random image from the local folder, and the cycle repeats.
- The key point is that the fullscreen image will only close when a new file is uploaded to the Google Drive folder, signaling the program to begin the next cycle after the timer ends.


### Troubleshooting

- If the image does not display, check the file path in your `.env` file to ensure it is correct.
- Ensure you’ve correctly set up Google API credentials by checking the `credentials.json` file.
- If you're having trouble with `tkinter` on Windows, run:

```bash
pip install tk  # For Windows users
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Mykal-Steele/ReMem/blob/main/LICENSE) file for details.
```

I hope this makes it easier for you to copy and use! If you need any more help, feel free to ask.
