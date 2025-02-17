# 🎥 ASCIImation 🎨

Turn YouTube videos into ASCII art right in your terminal!

## 🚀 Features

- **Download YouTube Videos**: Fetch videos directly from YouTube.
- **Extract Audio**: Extract audio from the video.
- **Convert to ASCII**: Transform video frames into ASCII art.
- **Play in Terminal**: Enjoy the video and audio playback in your terminal.

## 📦 Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/droidmaximus/asciimation.git
    cd asciimation
    ```
   > You can use the tool directly from the cloned repository by running the `asciimation.exe` file.

2. **Install the CLI Tool**:
    Make sure you have Python 3.6+ installed. Then, install the package using pip:
    ```sh
    pip install .
    ```

3. **Install FFmpeg**:
    Ensure you have FFmpeg installed on your system. You can download it from [FFmpeg's official website](https://ffmpeg.org/download.html).

4. **(Optional) Install the .exe**:
    If you want to create an executable file, run the following command:
    ```sh
    python build.py
    ```
    And you will get a .exe file in the `dist` folder, which you can run directly to use the tool.

## 🛠️ Usage

1. **Run the CLI Tool**:
    ```sh
    asciimation <YouTube-URL>
    ```

2. **Example**:
    ```sh
    asciimation https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ```

## 🤝 Contributing

We welcome contributions! Follow these steps to contribute:

1. **Fork the Repository**:
    Click the "Fork" button at the top right of this page.

2. **Clone Your Fork**:
    ```sh
    git clone https://github.com/droidmaximus/asciimation.git
    cd asciimation
    ```

3. **Create a Branch**:
    ```sh
    git checkout -b feature/your-feature-name
    ```

4. **Make Your Changes**:
    Implement your feature or fix a bug.

5. **Commit Your Changes**:
    ```sh
    git add .
    git commit -m "Add your descriptive commit message here"
    ```

6. **Push to Your Branch**:
    ```sh
    git push origin feature/your-feature-name
    ```

7. **Create a Pull Request**:
    Go to the original repository and click the "New Pull Request" button.

## 📝 Todo

- [ ] Add support for more video formats.
- [ ] Improve the speed of the ASCII conversion process.
- [ ] Add support for customizing the ASCII art output.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🌟 Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading YouTube videos.
- [pydub](https://github.com/jiaaro/pydub) for audio processing.
- [OpenCV](https://opencv.org/) for video frame processing.
- [FPSTimer](https://pypi.org/project/fpstimer/) for frame rate control.

---
Made with ❤️ by [Avinash](https://www.instagram.com/maxi.posting/)